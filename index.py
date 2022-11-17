import boto3
from botocore.exceptions import ClientError
def send_email(event):
    sender_id_domain = "demo.rishi-csye6225.me"
    SENDER = "noreply@" + sender_id_domain # must be verified in AWS SES Email
    RECIPIENT = event['RECIPIENT']
    token = event['token']
    user = event['user']
    print(user, RECIPIENT, token)
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # The subject line for the email.
    SUBJECT = "Verification of Email"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Hello {user}, Please verify your email".format(user=user) )
    BODY_HTML = """
    <html>
    <head></head>
    <body>
    <b>Link will be valid only for 5 minutes!</b></br>
    Find your link below:</p>
    <p><a href=http://demo.rishi-csye6225.me/v1/verifyUserEmail?email={RECIPIENT}&token={token} >
        http://demo.rishi-csye6225.me/v1/verifyUserEmail?email={RECIPIENT}&token={token} </a> </p>
        </body></html>
    </html>
                """.format(user=user,RECIPIENT=RECIPIENT,token=token)            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.

    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
    
                    'Data': BODY_HTML
                },
                'Text': {
    
                    'Data': BODY_TEXT
                },
            },
            'Subject': {

                'Data': SUBJECT
            },
        },
        Source=SENDER
    )

    print("Email sent! Message ID:")
    print(response['MessageId'])

def lambda_handler(event, context):
    # TODO implement
    send_email(event)