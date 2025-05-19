from shamir import Shamir

def split_secret(secret, n, k):
    shamir = Shamir()
    shares = shamir.split_secret(secret, n, k)
    return shares

def recover_secret(shares):
    shamir = Shamir()
    return shamir.recover_secret(shares)