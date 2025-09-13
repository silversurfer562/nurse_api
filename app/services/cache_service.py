"""
Caching service for the Nurse AI Assistant API.
"""
import json
import hashlib
from typing import Optional, Any, Dict
from datetime import timedelta
import redis.asyncio as redis
from app.config import settings
from loguru import logger


class CacheService:
    """Redis-based caching service."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.default_ttl = 3600  # 1 hour
    
    async def connect(self):
        """Connect to Redis."""
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            await self.redis_client.ping()
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Caching disabled.")
            self.redis_client = None
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis_client:
            await self.redis_client.close()
    
    def _generate_key(self, namespace: str, data: Dict[str, Any]) -> str:
        """Generate a cache key based on namespace and data."""
        # Create a consistent hash of the data
        data_str = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.md5(data_str.encode())
        return f"{namespace}:{hash_obj.hexdigest()}"
    
    async def get(self, namespace: str, data: Dict[str, Any]) -> Optional[str]:
        """Get cached data."""
        if not self.redis_client:
            return None
        
        try:
            key = self._generate_key(namespace, data)
            result = await self.redis_client.get(key)
            if result:
                logger.debug(f"Cache hit for key: {key}")
                return result
            else:
                logger.debug(f"Cache miss for key: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(
        self, 
        namespace: str, 
        data: Dict[str, Any], 
        value: str, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set cached data."""
        if not self.redis_client:
            return False
        
        try:
            key = self._generate_key(namespace, data)
            ttl = ttl or self.default_ttl
            await self.redis_client.setex(key, ttl, value)
            logger.debug(f"Cache set for key: {key}, TTL: {ttl}s")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, namespace: str, data: Dict[str, Any]) -> bool:
        """Delete cached data."""
        if not self.redis_client:
            return False
        
        try:
            key = self._generate_key(namespace, data)
            result = await self.redis_client.delete(key)
            logger.debug(f"Cache delete for key: {key}")
            return bool(result)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def clear_namespace(self, namespace: str) -> int:
        """Clear all keys in a namespace."""
        if not self.redis_client:
            return 0
        
        try:
            keys = await self.redis_client.keys(f"{namespace}:*")
            if keys:
                result = await self.redis_client.delete(*keys)
                logger.info(f"Cleared {result} keys from namespace: {namespace}")
                return result
            return 0
        except Exception as e:
            logger.error(f"Cache clear namespace error: {e}")
            return 0


# Global cache instance
cache_service = CacheService()