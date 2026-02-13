from mvg_api.v3.asyncapi import AsyncApi
from mvg_api.v3.syncapi import SyncApi


class SyncMVG(SyncApi):
    def __init__(self):
        super().__init__()


class AsyncMVG(AsyncApi):
    def __init__(self):
        super().__init__()
