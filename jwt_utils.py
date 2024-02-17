import base64
import hashlib
import hmac
import json
from flask import jsonify
from datetime import datetime, timedelta

def base64url_encode(data):
  return base64.urlsafe_b64encode(data).rstrip(b'=')

def create_jwt(user_id, secret):

  segments = []
    
  header = {"typ": "JWT", "alg": "HS256"}

  expiry = datetime.utcnow() + timedelta(hours=24)
  payload = {
    "user_id": user_id, 
    "exp": expiry.timestamp()
  }
  
  json_header = json.dumps(header, separators=(",",":")).encode()
  json_payload = json.dumps(payload, separators=(",",":")).encode()
  
  segments.append(base64url_encode(json_header))
  segments.append(base64url_encode(json_payload))
  
  signing_input = b'.'.join(segments)
  signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()

  segments.append(base64url_encode(signature))
                  
  encoded_string = b'.'.join(segments).decode()

  return encoded_string

def base64url_decode(input):
  rem = len(input) % 4
  if rem > 0:
    input += '=' * (4 - rem)
  return base64.urlsafe_b64decode(input)

def verify_jwt(jwt_token, secret):
  segments = jwt_token.split('.')
  header, payload, signature = segments

  # decoded_header = json.loads(base64url_decode(header).decode())
  decoded_payload = json.loads(base64url_decode(payload).decode())

  if datetime.utcnow().timestamp() <= decoded_payload['exp']:
    decoded_signature = base64url_decode(signature)

    signing_input = f"{header}.{payload}".encode()
    test_signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    
    if hmac.compare_digest(test_signature, decoded_signature):
      return jsonify({"message": "JWT valid"}), 200
    else: return jsonify({"error": "Forbidden, JWT invalid"}), 403

  else: return jsonify({"error": "Forbidden, token expired"}), 403

  

