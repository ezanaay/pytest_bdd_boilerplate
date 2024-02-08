# symmetric key program
from cryptography.fernet import Fernet


# Encryption
# key is generated using Fernet Key Generator
# key = Fernet.generate_key()
def encrypt(str, key):
    return Fernet(key).encrypt(str.encode())


# Decryption
# The same key that is used for encryption should be utilized for decryption
def decrypt(encrypted, key):
    return Fernet(key).decrypt(encrypted).decode()
