import time

CACHE_TTL = 300

cache = {}

def get_cache(key):
    item = cache.get(key)
    if not item:
        return None
    
    data, expiry = item

    if time.time() > expiry:
        del cache[key]
        return None
    
    return data

def set_cache(key, value):
    cache[key] = (value, time.time() + CACHE_TTL)