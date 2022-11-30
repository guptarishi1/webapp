variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "source_ami" {
  type    = string
  default = "ami-08c40ec9ead489470" # Ubuntu 22.04 LTS
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

variable "subnet_id" {
  type    = string
  default = "subnet-000ee724645978d81"
}



# https://www.packer.io/plugins/builders/amazon/ebs
source "amazon-ebs" "my-ami" {
  region     = "${var.aws_region}"
  ami_name        = "csye6225_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = "AMI for CSYE 6225"
  ami_users = ["022816248044","022816248044"]
  ami_regions = [
    "us-east-1",
  ]

  aws_polling {
    delay_seconds = 120
    max_attempts  = 50
  }


  instance_type = "t2.micro"
  source_ami    = "${var.source_ami}"
  ssh_username  = "${var.ssh_username}"
  subnet_id     = "${var.subnet_id}"

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
  }
}

build {

  sources = ["source.amazon-ebs.my-ami"]
  
  provisioner "file"{
  source = "default"
  destination = "/home/ubuntu/default"
  }

  provisioner "file"{
  source = "app.py"
  destination = "/home/ubuntu/app.py"
  }

  provisioner "file"{
  source = "test.service"
  destination = "/home/ubuntu/test.service"
  }

  provisioner "file"{
  source = "requirements.txt"
  destination = "/home/ubuntu/requirements.txt"
  }

  provisioner "file"{
  source = "dbconfig.json"
  destination = "/home/ubuntu/dbconfig.json"
  }

  provisioner "file"{
  source = "cloudwatch-config.json"
  destination = "/home/ubuntu/cloudwatch-config.json"
  }
  
  provisioner "file"{
  source = "script.sh"
  destination = "/home/ubuntu/script.sh"
  }

  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1"
    ] 

    scripts = fileset(".","script.sh")
      
    // type: "shell"
    // inline = [
      // "sudo apt-get update",
      // "sudo apt-get upgrade -y",
      // "sudo apt-get install nginx -y",
      // "sudo apt-get clean",
    // ]
  }
  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
