from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/healthz', methods=['GET'])
def home():
    return '''Hello 200 ok'''

@app.route('/', methods=['GET'])
def home1():
    return '''Hello'''

if(__name__=="__main__") :
    app.run()