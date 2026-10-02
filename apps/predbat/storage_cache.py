"""Shared safe access to Predbat's TTL-aware component cache."""

from storage import CacheResult


class StorageCacheMixin:
    """Provide common cache load/save error handling for API components.

    Subclasses set ``storage_module`` to their Storage namespace. Cache freshness
    and restoration policy remain with each integration.
    """

    storage_module = None
    storage_format = "yaml"
    storage_log_name = None

    async def save_cache(self, name, data, ttl_minutes=None, format="yaml"):
        """Save one cache entry, failing soft when storage is unavailable."""
        storage = self.storage
        if storage is None:
            return False
        try:
            return await storage.save_cached(self.storage_module, name, data, ttl_minutes=ttl_minutes, format=format if format != "yaml" else self.storage_format)
        except Exception as error:
            self.log(f"Warn: {self.storage_log_name or self.storage_module} could not save cache {name}: {error}")
            return False

    async def load_cache(self, name, ttl_minutes=None):
        """Load one cache entry, returning a CacheResult or None on a cache miss."""
        storage = self.storage
        if storage is None:
            return None
        try:
            return await storage.load_cached(self.storage_module, name, ttl_minutes=ttl_minutes)
        except Exception as error:
            self.log(f"Warn: {self.storage_log_name or self.storage_module} could not load cache {name}: {error}")
            self._restore_had_error = True
            return None

    async def age_cache(self, name):
        """Return a cache age for legacy callers, failing soft on storage errors."""
        storage = self.storage
        if storage is None:
            return None
        try:
            return await storage.age(self.storage_module, name)
        except Exception as error:
            self.log(f"Warn: {self.storage_log_name or self.storage_module} could not read cache age for {name}: {error}")
            self._restore_had_error = True
            return None

    @staticmethod
    def cache_value(result):
        """Return the cached value from a result, or None for a cache miss."""
        return result.value if isinstance(result, CacheResult) else None
