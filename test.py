from app.rate_limiters.fixed_window import FixedWindowRateLimiter

limiter = FixedWindowRateLimiter(limit=3, window_size=60)

for i in range(5):
    print(limiter.allow_request("test_user"))


# from pathlib import Path

# from app.redis_client import redis_client


# script = Path(
#     "app/lua/test.lua"
# ).read_text()

# result = redis_client.eval(
#     script,
#     0
# )

# print(result)