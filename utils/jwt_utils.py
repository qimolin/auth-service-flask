import base64
import json
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')

def create_jwt(user_id, private_key):
    segments = []
    
    header = {"typ": "JWT", "alg": "RS256"}  # Use RS256 for RSA signing

    expiry = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "user_id": user_id, 
        "exp": expiry.timestamp()
    }
  
    json_header = json.dumps(header, separators=(",", ":")).encode()
    json_payload = json.dumps(payload, separators=(",", ":")).encode()
  
    segments.append(base64url_encode(json_header))
    segments.append(base64url_encode(json_payload))
  
    signing_input = b'.'.join(segments)
    
    # Sign the data using the private key
    signature = private_key.sign(
        signing_input,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    segments.append(base64url_encode(signature))
                  
    encoded_string = b'.'.join(segments).decode()

    return encoded_string

def base64url_decode(input):
    rem = len(input) % 4
    if rem > 0:
        input += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input)

def verify_jwt(jwt_token, public_key):
    segments = jwt_token.split('.')
    header, payload, signature = segments

    decoded_payload = json.loads(base64url_decode(payload).decode())

    if datetime.utcnow().timestamp() <= decoded_payload['exp']:
        decoded_signature = base64url_decode(signature)
        signing_input = f"{header}.{payload}".encode()
        
        # Verify the signature using the public key
        try:
            public_key.verify(
                decoded_signature,
                signing_input,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return {"message": "JWT valid"}, 200
        except:
            return {"error": "Forbidden, JWT invalid"}, 403

    else:
        return {"error": "Forbidden, token expired"}, 403
