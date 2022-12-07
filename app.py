from urllib import response
from flask import Flask, jsonify, request, flash
from datetime import timedelta
from datetime import datetime
from functools import wraps
import bcrypt
import MySQLdb
from flask_mysqldb import MySQL
import re
from os import environ
from werkzeug.utils import secure_filename
import os
import urllib.request
from botocore.exceptions import ClientError
from flask import redirect,make_response, send_file
import boto3
import json
import sys
import botocore
import uuid
import MySQLdb
import time
from statsd import StatsClient

def init_db():
    app = Flask(__name__)  
    return app


app = init_db()

mysql = MySQL(app)

c = StatsClient()

with open("dbconfig.json", "r") as f:
    config = json.load(f)
    
app.config['s3_bucket'] = config['s3_bucket']
app.config['S3_LOCATION'] = 'http://{}.s3.us-east-1.amazonaws.com/'.format(config['s3_bucket'])

db=environ.get('db')
if db=="":
    print("ptest")
else:
  mysql= MySQLdb.connect(config['db_host'],config['db_user'],config['db_password'],config['default_database'])
  cursor=mysql.cursor()
  cursor.execute('CREATE TABLE if not exists customer (id varchar(255) PRIMARY KEY, Last_Name varchar(255) NOT NULL, First_Name varchar(255) NOT NULL, username varchar(255) NOT NULL UNIQUE, account_created  varchar(255), password varchar(255) NOT NULL,account_updated  varchar(255),account_verified int not null default (0))')
  mysql.commit()
  cursor.close()
  cursor=mysql.cursor()
  cursor.execute('Create TABLE if not exists document (doc_id varchar(255) PRIMARY KEY, user_id varchar(255), foreign key(user_id) references customer(id),name varchar(255) NOT NULL, date_created  varchar(255), s3_bucket_path varchar(255), versionId varchar(225))')
  mysql.commit()
  cursor.close()


from werkzeug.utils import secure_filename

@app.route('/healthz', methods=['GET'])
def home():
    start=time.time()

    app.logger.info("Hello 200 OK")
    dur = (time.time() - start)*1000
    c.timing("tasktime",dur)
    c.incr("taskcount")   

    return "Hello 200 ok"

@app.route('/', methods=['GET'])
def test1():
    start=time.time()

    app.logger.info("Hello 200 OK")
    dur = (time.time() - start)*1000
    c.timing("Open point",dur)
    c.incr("Open point count") 
    app.logger.info("Hello")
    return "Web development under progress"

@app.route('/v1/account/<string:id>', methods = ['GET'])

def home2(id):
    start=time.time()

    req_username = request.authorization.username
    if not validated_user(req_username):
        return "Please Verify the account - Action Unauthorized"

    cursor = mysql.cursor()

    # cursor.execute('SELECT id,Last_Name, First_Name, username, account_updated,account_created  FROM customer where id = %s',[id])
    cursor.execute('SELECT username, password FROM customer where id = %s',[id])
    
    output = list(cursor.fetchall())
    user = output[0]
    print(output)
    user1 = [user][0]
    pwd = user[1]
    print(user[1],user[0])
    
    

    if request.authorization and request.authorization.username != user[0]:
        return f"Forbidden Request", 403
    auth = request.authorization
    if not (auth):
        return"Unauthorized", 401
        
    cursor.close()
    
     
    auth_password = request.authorization.password.encode('utf-8')
    
    orig_password = user[1].encode('utf-8')
    
    password_check = bcrypt.checkpw(auth_password, orig_password)
    

    if not(request.authorization.username == user[0] and password_check):
        return f"Unauthorized", 401
    print('Authorized')
    

    cursor = mysql.cursor()
    cursor.execute('SELECT id, Last_Name, First_Name, username,account_updated,account_created FROM customer')
    output = cursor.fetchall()
    cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer WHERE id=%s',[id])
    output = cursor.fetchall()
    cursor.close()
    app.logger.info("GET Customer")

    dur = (time.time() - start)*1000
    c.timing("Get Customer duration",dur)
    c.incr("GET Customer")

    return jsonify(output)


@app.route('/v1/account/<string:id>', methods=['PUT'])
# @login_required
def update_emp(id):

    start=time.time()
    req_username = request.authorization.username
    if not validated_user(req_username):
        return "Please Verify the account - Action Unauthorized"
    
    app.logger.info("Hello 200 OK")
    

    _json = request.json 
    if len(_json) > 3 :
        return "Bad Request", 400

    _Last_Name = _json['Last_Name']
    _First_Name = _json['First_Name']
    _username = _json['username'] 
    date_time = datetime.now()
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    cursor = mysql.cursor()

    # cursor.execute('SELECT id,Last_Name, First_Name, username, account_updated,account_created  FROM customer where id = %s',[id])
    cursor.execute('SELECT username, password FROM customer where id = %s',[id])
    
    output = list(cursor.fetchall())
    user = output[0]

    user1 = user[0]
    pwd = user[1]
    print('password :', user[1], 'isername :', user[0])
    if request.authorization and request.authorization.username != user1:
        return f"Forbidden Request", 403
    auth = request.authorization
    if not (auth):
        return"Unauthorized", 401  
     
    auth_password = request.authorization.password.encode('utf-8')
    
    orig_password = pwd.encode('utf-8')
    
    password_check = bcrypt.checkpw(auth_password, orig_password)

    if not(request.authorization.username == user1 and password_check):
        return f"Unauthorized", 401
    
    print('Authorized')

 
    cursor.execute('SELECT count(username) FROM customer where username = %s',[_username])
    output = list(cursor.fetchall())    
    if output[0][0] >= 1 :
        return "email address already exists", 400

    sqlQuery = "UPDATE customer SET Last_Name=%s, First_Name=%s, username=%s, account_updated=%s  WHERE id=%s"
    bindData = (_Last_Name,_First_Name,_username,date_time,id)


    cursor.execute(sqlQuery, bindData)
    mysql.commit()

    cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer WHERE id=%s',[id])
    output = cursor.fetchall()

    cursor.close()
    
    respone = jsonify('Employee updated successfully!')
    respone.status_code = 200
    dur = (time.time() - start)*1000
    c.timing(" Counter",dur)
    c.incr("Put customer count")
    return jsonify(output),204

# lambda_client = boto3.client('lambda',
#                         region_name= 'us-east-1')


def validated_user(username):
    cursor=mysql.cursor()
    cursor.execute('SELECT username,account_verified FROM customer where username = %s',[username])
    output = list(cursor.fetchall())
    if output[0][1] == 1:
        return True
    return False

def check_token_expiry(table_items):
    print('table_items: ', table_items)
    dt = float(table_items['Creation_Time'])
    currentTime = float(time.time())
    time_diff_minutes = (currentTime - dt)/60
    if time_diff_minutes<=2.0:
        return True
    return False

def dynamo_db_insert(table_items,dynamodb_table,username):
    token = ""
    if not table_items:
        token = str(uuid.uuid4())
        response = dynamodb_table.put_item(
        Item={
            'TokenName': token,
            'Email': username,
            'Creation_Time' : str(time.time()),
            'Expiration_Time' : str(time.time() + 120)
            }
        )
        print("New record inserted successfully")
        print('response: ', response)
        snspublish(username, token)
    else:
        token = table_items['token']
    return token

def snspublish(username, token):
    sns = boto3.client('sns', region_name = 'us-east-1')
    att_dict={}
    att_dict['Email'] = {'DataType':'String','StringValue':username}
    att_dict['Token'] = {'DataType':'String','StringValue':token}
    sns.publish(TopicArn='arn:aws:sns:us-east-1:022816248044:verify_email', Message="message to sns to verify user", Subject="verify your email", MessageAttributes=att_dict)

# # lambda_client = boto3.client('lambda',
# #                         region_name= 'us-east-1')


# def send_verification_email(token, user, user_email):
#     payload = {'token':token, 
#                 'user':user,
#                 'RECIPIENT':user_email}
#     result = lambda_client.invoke(FunctionName='verifyEmail',
#                                     Payload=json.dumps(payload))
    
#     return result

@app.route('/v2/account', methods=['POST'])
def create_cust():

 
    # try: 
    start=time.time()
    app.logger.info("Hello 200 OK")           
    _json = request.json
    _Last_Name = _json['Last_Name']
    _First_Name = _json['First_Name']
    _username = _json['username'] 
    _password = _json['password'] 

    _id = str(uuid.uuid4())
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(_password.encode('utf-8'), salt)

    date_time = datetime.now()
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    print(date_time)

    _account_updated = date_time
    _account_created = date_time

    cursor = mysql.cursor()	

    cursor.execute('SELECT count(username) FROM customer where username = %s',[_username])
    output = list(cursor.fetchall())
    print('output: ', output)

    cursor.execute('SELECT username,account_verified FROM customer where username = %s',[_username])
    output = list(cursor.fetchall())

    dynamodb_client = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb_table = dynamodb_client.Table('csye6225Pro2')
    # table_items = dynamodb_table.get_item(Key={'Email':_username})['Item']
    table_items = ''
    print ('table_items: ', table_items)

    print('output: ', output)
    if output:
        if output[0][1] == 0:
            return "Verification Pending", 201
        elif output[0][1] == 1: 
            return "Verified User Already Exists", 400

    token = dynamo_db_insert(table_items,dynamodb_table, _username)   

    
    cursor.execute('INSERT INTO customer(id, Last_Name,First_Name,username,password,account_updated,account_created) VALUES(%s,%s, %s,%s, %s,%s,%s)',(_id,_Last_Name,_First_Name,_username,hash_pwd.decode('utf-8'), date_time, date_time))
    # print(bcrypt.check_password_hash(hashVar_pwd, '_password'))
    mysql.commit()

    cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer where username = %s',[_username])
    output = cursor.fetchall()

    respone = jsonify('Customer added successfully!')
    respone.status_code = 200

    # result = send_verification_email(token,_First_Name, _username)
    # print ('result: ', result)

    dur = (time.time() - start)*1000
    c.timing("Post Timing",dur)
    c.incr("Post count")
       
    return jsonify(output), 201 


s3 = boto3.client('s3')

BUCKET_NAME=config['s3_bucket']


def upload_to_s3(fileObject, filename, bucket_name, doc_id, user_id):
    print("type(fileObject): ",type(fileObject))
    filepath = os.path.join(user_id,doc_id,filename)

    VersionId = s3.put_object(
            Body=fileObject,
            Bucket=bucket_name,
            Key=filepath
        )['VersionId']
    print("VersionId: ",VersionId)
    return os.path.join(app.config['S3_LOCATION'],filepath), VersionId

def delete_file_from_s3(file, bucket_name,doc_id, user_id, VersionId):
    filepath = os.path.join(user_id,doc_id,file)
    print("deleting: ",filepath)
    output = s3.delete_objects(Bucket=bucket_name,Delete={'Objects':[{'Key':filepath,'VersionId':VersionId}],'Quiet':False})
    print("delete output: ",output)

@app.route('/v1/documents', methods = ['GET'])
def show_docs():
    start=time.time()

    app.logger.info("Hello 200 OK")

    req_username = request.authorization.username
    if not validated_user(req_username):
        return "Please Verify the account - Action Unauthorized"

    cursor = mysql.cursor()
    username = request.authorization.username
    cursor.execute('SELECT id, username, password FROM customer WHERE username = %s',[username])
    return_val = list(cursor.fetchall())
    user_data = {
        'id': return_val[0][0],
        'username': return_val[0][1]
    }

    bind_names = ('doc_id','user_id','name','date_created','s3_bucket_path')
    cursor.execute('SELECT * FROM document WHERE user_id = %s',[user_data['id']])
    doc_data = list(cursor.fetchall())
    
    mysql.commit()
    cursor.close()
    json_data = []
    for x in doc_data:
        json_data.append(dict(zip(bind_names, x)))

    dur = (time.time() - start)*1000
    c.timing("Get Doc Timing",dur)
    c.incr("Get Doc count") 

    return jsonify(json_data)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/v1/documents', methods = ['POST'])
def upload_file():
    start=time.time()

    req_username = request.authorization.username
    if not validated_user(req_username):
        return "Please Verify the account - Action Unauthorized" 

    cursor = mysql.cursor()
    username = request.authorization.username
    cursor.execute('SELECT id, username, password FROM customer WHERE username = %s',[username])
    return_val = list(cursor.fetchall())
    print(return_val)
    user_data = {
        'id': return_val[0][0],
        'username': return_val[0][1]
    }

    
    print(username)
    if not request.authorization:
        return f"Basic auth missing", 403
    else:
        # Authorization
        auth_password = request.authorization.password.encode('utf-8')
        print("auth_password: ",auth_password)
        orig_password = return_val[0][2].encode('utf-8')
        print("orig_password: ",orig_password)
        password_check = bcrypt.checkpw(auth_password, orig_password)
        print("Password check: ",password_check)
        if not(password_check):
            return f"Unauthorized", 401
        print('Authorized')
    
    if "user_file" not in request.files:
        return "user file  key is not in request.files"

    file = request.files["user_file"]

    if file.filename == "":
        return "Kindly select the file"
    
    date_time = datetime.now()
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    if file:
        file.filename = secure_filename(file.filename)
        
        resp_data = {}
        resp_data['doc_id'] = str(uuid.uuid4())
        resp_data['user_id'] = user_data['id']
        s3_bucket_path, versionId = upload_to_s3(file.read(), file.filename, app.config["s3_bucket"],resp_data['doc_id'],resp_data['user_id'])
        resp_data['name'] = file.filename
        resp_data['date_created'] = date_time
        resp_data['s3_bucket_path'] = s3_bucket_path
    cursor.execute("INSERT INTO document(doc_id, user_id, name, date_created, s3_bucket_path, versionId) VALUES('{doc_id}','{user_id}','{name}','{date_created}','{s3_bucket_path}','{versionId}')" .format(doc_id = resp_data['doc_id'], user_id = resp_data['user_id'], name = resp_data['name'], date_created = resp_data['date_created'], s3_bucket_path = resp_data['s3_bucket_path'], versionId =versionId))
    mysql.commit()
    cursor.close() 

    app.logger.info("Hello 200 OK")
    dur = (time.time() - start)*1000
    c.timing("Post Doc Timing",dur)
    c.incr("Post Doc count")  
    return jsonify(resp_data)

    
@app.route('/v1/documents/<doc_id>', methods = ['GET'])
def get_docs(doc_id): 

    start=time.time()

    app.logger.info("Hello 200 OK")

    req_username = request.authorization.username
    if not validated_user(req_username):
        return "Please Verify the account - Action Unauthorized"

    cursor = mysql.cursor()
    username = request.authorization.username
    cursor.execute('SELECT id, username, password FROM customer WHERE username = %s',[username])
    return_val = list(cursor.fetchall())
    # user_data = {
    #     'id': return_val[0][0],
    #     'username': return_val[0][1]
    # }

    
    print(username)
    if not request.authorization:
        return f"Basic auth missing", 403
    else:
          

        # Authorization
        auth_password = request.authorization.password.encode('utf-8')
        print("auth_password: ",auth_password)
        orig_password = return_val[0][2].encode('utf-8')
        print("orig_password: ",orig_password)
        password_check = bcrypt.checkpw(auth_password, orig_password)
        print("Password check: ",password_check)
        if not(password_check):
            return f"Unauthorized", 401
        print('Authorized')

    cursor.execute('SELECT doc_id,user_id,name,date_created,s3_bucket_path FROM document WHERE doc_id = %s',[doc_id])
    return_val = cursor.fetchall()
    # print(return_val)
    # json_output = {
    #     'doc_id': return_val[0]['doc_id'],
    #     'id': return_val[0]['user_id'],
    #     'name': return_val[0]['name'],
    #     'date_created': return_val[0]['date_created'],
    #     's3_bucket_path': return_val[0]['s3_bucket_path']
    # }

    cursor.close()

    # output = download(doc_id, BUCKET)
    # downloadfile = send_file(output, as_attachment=True)
    dur = (time.time() - start)*1000
    c.timing("Get from Doc ID timing",dur)
    c.incr("Get from Doc ID  count") 

    return jsonify(return_val)    


@app.route('/v1/documents/<doc_id>', methods = ['DELETE'])
def delete_file(doc_id):

    start=time.time()

    app.logger.info("Hello 200 OK")

    req_username = request.authorization.username
    if not validated_user(req_username):
        return "Please Verify the account - Action Unauthorized"   

    cursor = mysql.cursor()
    username = request.authorization.username
    cursor.execute('SELECT id, username, password FROM customer WHERE username = %s',[username])
    return_val = list(cursor.fetchall())
    # user_data = {
    #     'id': return_val[0][0],
    #     'username': return_val[0][1]
    # }

    
    print(username)
    if not request.authorization:
        return f"Basic auth missing", 403
    else:
          

        # Authorization
        auth_password = request.authorization.password.encode('utf-8')
        print("auth_password: ",auth_password)
        orig_password = return_val[0][2].encode('utf-8')
        print("orig_password: ",orig_password)
        password_check = bcrypt.checkpw(auth_password, orig_password)
        print("Password check: ",password_check)
        if not(password_check):
            return f"Unauthorized", 401
        print('Authorized')

    cursor.execute('SELECT * FROM document WHERE doc_id = %s',[doc_id])
    return_val = list(cursor.fetchall())
    doc_data = {
        'doc_id': return_val[0][0],
        'user_id': return_val[0][1],
        'name': return_val[0][2],
        's3_bucket_path': return_val[0][3],
        'versionId': return_val[0][4]
    }
    delete_file_from_s3(doc_data['name'], app.config["s3_bucket"],doc_id, doc_data['user_id'], doc_data['versionId'])
    cursor.execute('DELETE FROM document WHERE doc_id = %s',[doc_id])

    mysql.commit()
    cursor.close()  
    
    dur = (time.time() - start)*1000
    c.timing("Deleting the Document Timing",dur)
    c.incr("Deleting the Document count")    

    return jsonify({"MESSAGE":"FILE DELETED"})
from boto3.dynamodb.conditions import Key
@app.route('/v1/verifyUserEmail',methods = ['GET'])
def verify_user():
    user_email=request.args.get('Email')
    token = request.args.get('Token')
    dynamodb_client = boto3.resource('dynamodb',region_name='us-east-1')
    dynamodb_table = dynamodb_client.Table('csye6225Pro2')
    # table_items = dynamodb_table.query(
    #     KeyConditionExpression=Key('Email').eq(user_email),Key('TokenName').eq(token)
    # )
    table_items = dynamodb_table.get_item(Key={'Email':user_email, 'TokenName':token})['Item']
    token_verified = check_token_expiry(table_items)
    cursor=mysql.cursor()
    if token_verified:   
        cursor.execute('UPDATE customer SET account_verified = 1 WHERE username = %s',[user_email])
        mysql.commit()
        
        return f"User Successfully Verified"
    
    cursor.execute('DELETE FROM customer WHERE username = %s',[user_email])
    mysql.commit()
    cursor.close() 
    return f"Token Expired" 

with app.app_context():
    print('connection setup')    
    # conn = mysql.connection

if(__name__=="__main__") :
    
    app.run(debug=True)

