import bcrypt

def get_hash_password(password: str) -> str:
    pw_bytes = password[:72].encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode("utf‑8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password[:72].encode("utf‑8")
    hash_bytes = hashed_password.encode("utf‑8")
    return bcrypt.checkpw(pw_bytes, hash_bytes)
