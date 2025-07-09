import os
from pydantic import BaseModel
import redis

class CacheManager(BaseModel):
    r: redis.Redis
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_env(cls):
        """
        Create an instance of CacheManager using environment variables.
        """
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))

        return cls(
            r=redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        )

    def set(self, key: str, value: str):
        """
        Set a value in the Redis cache.
        """
        self.r.set(key, value)
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the Redis cache.
        """
        print(f"Checking existence of key: {key}")
        return bool(self.r.exists(key))