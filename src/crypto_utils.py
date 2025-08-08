import bcrypt


def encyptPassword(plaintext: str) -> bytes:
    salt = bcrypt.gensalt(rounds=5)
    return bcrypt.hashpw(plaintext.encode("utf8"), salt)


def checkPassword(plaintext: str, cipherbytes: bytes) -> bool:
    return bcrypt.checkpw(plaintext.encode("utf8"), cipherbytes)
