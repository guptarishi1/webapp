from urllib import response
from flask import Flask, jsonify, request, flash
import pymysql
from flask_mysqldb import MySQL
from datetime import timedelta
from datetime import datetime
from functools import wraps
import bcrypt
from unicodedata import name

def init_db():
    app = Flask(__name__)
    return app


app = init_db()




app.config['MYSQL_USER'] = 'FlaskDB'
app.config['MYSQL_PASSWORD'] = 'FlaskDB@12345678'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'FlaskDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



mysql = MySQL(app)


@app.route('/healthz', methods=['GET'])
def home():

    return "Hello 200 ok"


@app.route('/v1/account/<string:id>', methods = ['GET'])

def home2(id):

    conn = mysql.connection
    cur = mysql.connection.cursor()

    # cur.execute('SELECT id,Last_Name, First_Name, username, account_updated,account_created  FROM customer where id = %s',[id])
    cur.execute('SELECT username, password FROM customer where id = %s',[id])
    
    output = cur.fetchall()
    user = output[0]

    user1 = user["username"]
    pwd = user["password"]
    print(user["password"],user["username"])
    
    

    if request.authorization and request.authorization.username != user["username"]:
        return f"Forbidden Request", 403
    auth = request.authorization
    if not (auth):
        return"Unauthorized", 401
        
    cur.close()
    
     
    auth_password = request.authorization.password.encode('utf-8')
    
    orig_password = user["password"].encode('utf-8')
    
    password_check = bcrypt.checkpw(auth_password, orig_password)
    
    # username = output['username']
    # if not(request.authorization):
    #     return f"wrong Authorization"
    if not(request.authorization.username == user["username"] and password_check):
        return f"Unauthorized", 401
    print('Authorized')
    


    # if request.authorization and request.authorization.username == username and request.authorization.password == password:
    # #     return  output 
    # username = output['username']
    # if request.authorization and request.authorization.username != username:
    #     return f"Forbidden Request", 403
    conn = mysql.connection
    cur = mysql.connection.cursor()

    cur.execute('SELECT id, Last_Name, First_Name, username,account_updated,account_created FROM customer')
    output = cur.fetchall()

    conn = mysql.connection
    cursor = conn.cursor()	

    cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer WHERE id=%s',[id])
    output = cursor.fetchall()

    return jsonify(output)

    


@app.route('/', methods = ['GET'])
# @login_required
def home1():

    conn = mysql.connection
    cur = mysql.connection.cursor()

    cur.execute('SELECT id, Last_Name, First_Name, username,account_updated,account_created FROM customer')
    output = cur.fetchall()
    
    conn.commit()
    
    cur.close()

    

    return  jsonify(output)



#    cur.execute('''CREATE TABLE Customer(Id INTEGER, name VARCHAR(20))''')
    # return '''ok 2'''



@app.route('/v1/account/<string:id>', methods=['PUT'])
# @login_required
def update_emp(id):

    _json = request.json 
    if len(_json) > 3 :
        return "Bad Request", 400

    
    # _id = _json['id']
    # _name = _json['name']
    _Last_Name = _json['Last_Name']
    _First_Name = _json['First_Name']
    _username = _json['username'] 
    date_time = datetime.now()
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # _password = _json['_password']
    # if _name and _id and request.method == 'PUT':		
    
    

    conn = mysql.connection
    cur = mysql.connection.cursor()

    # cur.execute('SELECT id,Last_Name, First_Name, username, account_updated,account_created  FROM customer where id = %s',[id])
    cur.execute('SELECT username, password FROM customer where id = %s',[id])
    
    output = cur.fetchall()
    user = output[0]

    user1 = user["username"]
    pwd = user["password"]
    print(user["password"],user["username"])
    if request.authorization and request.authorization.username != user["username"]:
        return f"Forbidden Request", 403
    auth = request.authorization
    if not (auth):
        return"Unauthorized", 401
    
    cur.close()
    
     
    auth_password = request.authorization.password.encode('utf-8')
    
    orig_password = user["password"].encode('utf-8')
    
    password_check = bcrypt.checkpw(auth_password, orig_password)
    
    # username = output['username']
    # if not(request.authorization):
    #     return f"wrong Authorization"
    if not(request.authorization.username == user["username"] and password_check):
        return f"Unauthorized", 401
    
    print('Authorized')


    
    
    conn = mysql.connection
    cursor = conn.cursor()	
    cursor.execute('SELECT count(username) FROM customer where username = %s',[_username])
    output = cursor.fetchall()    
    if output[0]["count(username)"] >= 1 :
        return "email address already exists", 400
    
    
    


    sqlQuery = "UPDATE customer SET Last_Name=%s, First_Name=%s, username=%s, account_updated=%s  WHERE id=%s"
    bindData = (_Last_Name,_First_Name,_username,date_time,id)
    conn = mysql.connection
    cur = mysql.connection.cursor()
    cur.execute(sqlQuery, bindData)
    conn.commit()

    conn = mysql.connection
    cursor = conn.cursor()	

    cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer WHERE id=%s',[id])
    output = cursor.fetchall()
    
    respone = jsonify('Employee updated successfully!')
    respone.status_code = 200
    return jsonify(output),204




@app.route('/v1/account', methods=['POST'])
def create_cust():

    # try:        
        _json = request.json
        _Last_Name = _json['Last_Name']
        _First_Name = _json['First_Name']
        _username = _json['username'] 
        _password = _json['password'] 
        conn = mysql.connection
        cursor = conn.cursor()
        # cursor = conn.cursor()
        cursor.execute('CREATE TABLE if not exists customer (id int not null AUTO_INCREMENT PRIMARY KEY, Last_Name varchar(255) NOT NULL, First_Name varchar(255) NOT NULL, username varchar(255) NOT NULL UNIQUE, account_created  varchar(255), password varchar(255) NOT NULL,account_updated  varchar(255))')
        conn.commit()
        cursor.close()

        salt = bcrypt.gensalt()
        hash_pwd = bcrypt.hashpw(_password.encode('utf-8'), salt)

    
        date_time = datetime.now()
        date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        print(date_time)

        _account_updated = date_time
        _account_created = date_time

        conn = mysql.connection
        cursor = conn.cursor()	

        cursor.execute('SELECT count(username) FROM customer where username = %s',[_username])
        output = cursor.fetchall()

        
        if output[0]["count(username)"] >= 1 :
            return "Bad Request", 400
        
    
        sqlQuery = "INSERT INTO customer(Last_Name,First_Name,username,password,account_updated,account_created) VALUES(%s, %s,%s, %s,%s,%s)"
        bindData = (_Last_Name,_First_Name,_username,_password, date_time, date_time)           
        cursor.execute('INSERT INTO customer(Last_Name,First_Name,username,password,account_updated,account_created) VALUES(%s, %s,%s, %s,%s,%s)',(_Last_Name,_First_Name,_username,hash_pwd.decode('utf-8'), date_time, date_time))
        # print(bcrypt.check_password_hash(hashVar_pwd, '_password'))
        conn.commit()

        conn = mysql.connection
        cursor = conn.cursor()	

        cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer where username = %s',[_username])
        output = cursor.fetchall()

        respone = jsonify('Customer added successfully!')
        respone.status_code = 200
        return jsonify(output), 201 

    # except Exception as e:
    #     print(e)

with app.app_context():
    print('connection setup')    
    # conn = mysql.connection



if(__name__=="__main__") :
    
    app.run(debug=True)

