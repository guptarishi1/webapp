from urllib import response
from flask import Flask, jsonify, request, flash
import pymysql
from flask_mysqldb import MySQL
from datetime import timedelta
from datetime import datetime
from functools import wraps
import bcrypt

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

# def check_auth(username, password):

#     return username == 'Rishi' and password == '1234'

# def login_required(f):
#     """ basic auth for api """
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(id,auth.username, auth.password):
#             return jsonify({'message': 'Authentication required'}), 401
#         return f(*args, **kwargs)
#     return decorated_function

@app.route('/v1/account/<string:id>', methods = ['GET'])
# @login_required()
def home2(id):

    conn = mysql.connection
    cur = mysql.connection.cursor()

    cur.execute('SELECT id,Last_Name, First_Name, username, account_updated,account_created  FROM customer where id = %s',[id])
    output = cur.fetchall()
     
    # conn.commit()
    # cur.close()
    # # username = output['username']
    # # password = output['password']

    # # print('username: ', username)
    # # print('password:', password)


    

    # # if request.authorization and request.authorization.username == username and request.authorization.password == password:
    # #     return  output 
    # username = output['username']
    # if request.authorization and request.authorization.username != username:
    #     return f"Forbidden Request", 403
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
    # _id = _json['id']
    # _name = _json['name']
    _Last_Name = _json['Last_Name']
    _First_Name = _json['First_Name']
    _username = _json['username'] 
    date_time = datetime.now()
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # _password = _json['_password']
    # if _name and _id and request.method == 'PUT':		
    if len(_json) > 3:
        return "Attempt to update any other field", 400
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

    cursor.execute('SELECT id,Last_Name,First_Name,username,account_updated,account_created FROM customer where username = %s',[_username])
    output = cursor.fetchall()
    
    respone = jsonify('Employee updated successfully!')
    respone.status_code = 200
    return jsonify(output)




@app.route('/v1/account', methods=['POST'])
def create_cust():
    # try:        
        _json = request.json
        _Last_Name = _json['Last_Name']
        _First_Name = _json['First_Name']
        _username = _json['username'] 
        _password = _json['password'] 

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
            return "email address already exists", 400
        

        
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
        return jsonify(output) 

    # except Exception as e:
    #     print(e)





if(__name__=="__main__") :
    app.run(debug=True)

