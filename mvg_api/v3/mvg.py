from mvg_api.v3.asyncapi import AsyncApi
from mvg_api.v3.syncapi import SyncApi


class SyncMVG(SyncApi):
    def __init__(self, do_log_responses: bool = False):
        """
        Creates a new API instance to send requests the MVG backend.
        This instance can be used to send multiple requests, thereby reusing the http client.

        :param do_log_responses: whether the responses of the MVG api should be logged for debugging purposes.
        """
        super().__init__(do_log_responses=do_log_responses)


class AsyncMVG(AsyncApi):
    def __init__(self, do_log_responses: bool = False):
        """
        Creates a new API instance to send requests the MVG backend.
        This instance can be used to send multiple requests, thereby reusing the http client.

        :param do_log_responses: whether the responses of the MVG api should be logged for debugging purposes.
        """
        super().__init__(do_log_responses=do_log_responses)
