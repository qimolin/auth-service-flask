import os
from os.path import join, dirname
from dotenv import load_dotenv
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_PRIVATE_KEY_PASSWORD = os.getenv("PRIVATE_KEY_PASSWORD")

# Generate a new RSA key pair
def generate_key_pair():
    private_key_path = "private.pem"
    public_key_path = "public.pem"
    
    # Check if key pair already exist
    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        print("Key pair already exist.")
        return

    # Generate new key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Write private key to file
    with open(private_key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(_PRIVATE_KEY_PASSWORD.encode())
            )
        )

    # Write public key to file
    public_key = private_key.public_key()
    with open(public_key_path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

# Load private key from file
def load_private_key():
    private_key_path = "private.pem"
    with open(private_key_path, 'rb') as f:
        private_key_data = f.read()
    return serialization.load_pem_private_key(
        private_key_data,
        password=_PRIVATE_KEY_PASSWORD.encode(),
        backend=default_backend()
    )

# Load public key from file
def load_public_key():
    public_key_path = "public.pem"
    with open(public_key_path, 'rb') as f:
        public_key_data = f.read()
    return serialization.load_pem_public_key(
        public_key_data,
        backend=default_backend()
    )
