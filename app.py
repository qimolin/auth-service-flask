from flask_pymongo import PyMongo
from flask import Flask, request
from flask_bcrypt import Bcrypt
from utils.jwt_utils import create_jwt, verify_jwt
from utils.rsa_key_utils import generate_key_pair, load_private_key, load_public_key

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["MONGO_URI"] = "mongodb://root:example@mongo:27017/authDatabase?authSource=admin"
mongo = PyMongo(app)

generate_key_pair()

private_key = load_private_key()

@app.post('/users')
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({"username": username}):
        return {"detail": "duplicate"}, 409

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')

    mongo.db.users.insert_one({
        "username": username,
        "password": encrypted_password
    })

    return {"message": "User registered successfully"}, 201

@app.put('/users')
def update_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    new_password = data.get('new_password')
    
    if password == new_password:
        return {"detail": "forbidden"}, 403

    user =  mongo.db.users.find_one({"username": username})
    
    if not user:
        return {"detail": "forbidden"}, 403

    hashed_password = user['password']
    
    if bcrypt.check_password_hash(hashed_password, password):
        new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        updated = mongo.db.users.update_one({"username": username}, {"$set": {"password": new_hashed_password}})
        if updated.modified_count > 0:
            return {"message": "Password updated successfully"}, 200
        else:
            return {"detail": "forbidden"}, 403
    else:
        return {"detail": "forbidden"}, 403
    
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
            return {"detail": "forbidden"}, 403
    else:
        return {"detail": "forbidden"}, 403

@app.post('/auth')
def verify_auth():
    data = request.get_json()
    token = data.get('token')
    
    # Load public key
    public_key = load_public_key()

    # Verify the JWT token
    result = verify_jwt(token, public_key)
    
    if 'error' in result:
        return {'valid': False}, 403
    else: 
        return {'valid': True, 'user_id': result['user_id']}, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)