From flask import Flask
app = Flask(__name__)

@app.route('/verify')
def verify():
    return 'TBD'

@app.route('/login')
def login():
    return 'TBD'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
