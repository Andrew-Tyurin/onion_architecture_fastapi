import os

from dotenv import load_dotenv

load_dotenv()


def is_admin(password: str) -> bool:
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_password == password:
        return True
    return False
