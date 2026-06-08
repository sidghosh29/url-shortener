from pathlib import Path
# import sys
# import os
# sys.path.append(os.path.abspath("./"))
# print(sys.path)
from app.config import settings
from app.redis_client import redis_client

# LUA_SCRIPT_PATH = settings.LUA_FOLDER_PATH+"/fixed_window.lua"
LUA_SCRIPT_PATH = (
    Path(settings.LUA_FOLDER_PATH)
    / "fixed_window.lua"
)

LUA_SCRIPT = Path(LUA_SCRIPT_PATH).read_text()

class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size

    def allow_request(self, key: str) -> bool:
        result = redis_client.eval(LUA_SCRIPT, 1, key, self.limit, self.window_size)

        return bool(result)
    

fixed_window_limiter = FixedWindowRateLimiter(
    limit=10,
    window_size=60
)