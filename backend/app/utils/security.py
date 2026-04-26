import hashlib
import uuid

def generate_hash():
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()