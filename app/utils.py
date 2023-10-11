import bcrypt

def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    # Check if the plain password matches the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# from passlib.context import CryptContext

# pdw_contexte = CryptContext(schemes=['bcrypt'], deprecated="auto")
# def hash_password(password: str):
#     return pdw_contexte.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pdw_contexte.verify(plain_password, hashed_password)