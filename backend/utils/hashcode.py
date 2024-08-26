import hashlib

def hashcode(s, salt = 'somethingouthere'):
    sha256_hash = hashlib.new('sha256')
    s += salt
    sha256_hash.update(s.encode())
    return sha256_hash.hexdigest()