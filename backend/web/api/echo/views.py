from fastapi import APIRouter, Depends
from redis.asyncio import ConnectionPool, Redis

from backend.web.api.echo.schema import Message
from backend.services.redis.dependency import get_redis_pool

router = APIRouter()


@router.post("/", response_model=Message)
async def send_echo_message(
    incoming_message: Message,
    redis_pool: ConnectionPool = Depends(get_redis_pool),
) -> Message:
    """
    Sends echo back to user.
    First checks if the key exists in Redis cache.
    If it exists, returns product IDs from Redis.
    If not, performs operations and saves result to Redis.

    :param incoming_message: incoming message.
    :param redis_pool: redis connection pool.
    :returns: message same as the incoming.
    """
    # Use the incoming message as the Redis key
    key = f"echo:{incoming_message.message}"
    
    # Check if key exists in Redis
    async with Redis(connection_pool=redis_pool) as redis:
        cached_value = await redis.get(key)
        
        if cached_value:
            # If found in cache, return the cached product IDs
            return Message(
                message=f"From cache: {cached_value.decode('utf-8')}"
            )
        
        # If not in cache, perform normal operations
        # Here we're just echoing the message back, but in a real scenario
        # you would perform product search operations and get product IDs
        
        # Save the result to Redis for future use
        result = incoming_message.message
        await redis.set(key, result)
        
        return incoming_message
