from flask_pymongo import PyMongo
from flask import Flask, request, abort
from flask_bcrypt import Bcrypt
from utils.jwt_utils import create_jwt
from utils.rsa_key_utils import generate_key_pair, load_private_key, load_public_key
from cryptography.hazmat.primitives import serialization


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/authDatabase"
mongo = PyMongo(app)

generate_key_pair()

private_key = load_private_key()

@app.post('/users')
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({"username": username}):
        return {"error": "Duplicate username"}, 409

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    mongo.db.users.insert_one({
        "username": username,
        "password": encrypted_password
    })

    return {"message": "User registered successfully"}, 201

@app.put('/users')
def update_password():
    # TODO: Implement password update
    pass

@app.post('/users/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # get user from DB
    user = mongo.db.users.find_one({"username": username})

    if user:
        if bcrypt.check_password_hash(user['password'], password):
            token = create_jwt(str(user['_id']), private_key)
            return {"token": token}, 200  # Return the JWT token
        else:
            return abort(403)
    else:
        return abort(403)

# Can be made more secure using k8s secrets
@app.get('/public-key')
def get_public_key():
    public_key = load_public_key()
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return {"public_key": pem_public_key}, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)