import asyncio
from config import Settings, settings

def config_nodes(function, config: Settings = settings):
    if asyncio.iscoroutinefunction(function):
        async def wrapper(state):
            return await function(state, config)
        return wrapper
    else:
        def wrapper(state):
            return function(state, config)
        return wrapper