```python
import random
import string
import base64

def generate_short_id() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def to_base64(short_id: str) -> str:
    return base64.b64encode(short_id.encode()).decode()
```