import bcrypt

#hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

#verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())
