local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local now = tonumber(redis.call("TIME")[1])

local data = redis.call(
    "HMGET",
    key,
    "tokens",
    "last_refill"
)

local tokens = tonumber(data[1])
local last_refill = tonumber(data[2])

-- First request
if not tokens then
    tokens = capacity
    last_refill = now
end

-- Calculate earned tokens
local refill_rate = capacity / window

local elapsed = now - last_refill

local earned = math.floor(
    elapsed * refill_rate
)

tokens = math.min(
    capacity,
    tokens + earned
)

-- Advance refill timestamp
if earned > 0 then
    last_refill = now
end

-- Reject if no tokens
if tokens < 1 then
    redis.call(
        "HMSET",
        key,
        "tokens",
        tokens,
        "last_refill",
        last_refill
    )

    redis.call("EXPIRE", key, window * 2)

    return 0
end

-- Consume one token
tokens = tokens - 1

redis.call(
    "HMSET",
    key,
    "tokens",
    tokens,
    "last_refill",
    last_refill
)

redis.call("EXPIRE", key, window * 2)

return 1