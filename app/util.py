from hashlib import sha512
import random



def hash_pass(password, salt="SALT"):
    new_pw = password + salt
    hashed_pw = sha512(new_pw.encode()).hexdigest()
    return hashed_pw

def generate_key(length=15):
    seed = (str(random.random()) + str(random.random())).encode()
    hashed_output = sha512(seed).hexdigest()
    return hashed_output[:length]