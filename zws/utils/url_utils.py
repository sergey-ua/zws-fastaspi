package zws.utils

from urllib.parse import urlparse
import base64
import random
import string

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def to_base64(short_id: str) -> str:
    return base64.b64encode(short_id.encode()).decode()

def generate_short_id() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))