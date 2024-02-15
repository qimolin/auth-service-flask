from flask import Flask

app = Flask(__name__)

app.post('/users')
def register():
    # TODO: Implement registration
    pass

app.put('/users')
def update_password():
    # TODO: Implement password update
    pass

app.post('/users/login')
def login():
    # TODO: Implement login
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)