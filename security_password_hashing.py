import hashlib

def generate_encrypted_hash(password: str) -> str:
    hash = hashlib.sha512(bytes(password, "utf-8"))
    return hash.hexdigest()
