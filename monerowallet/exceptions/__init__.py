"""
    The ``exceptions`` module
    =============================
 
    Exceptions raised by PyMoneroWallet.
 
"""

class Error(Exception):
    '''
        General PyMoneroWallet exception
    '''
    pass


class StatusCodeError(Error):
    '''
        Returned when HTTP status code is different from 200
    '''
    pass


class Unauthorized(StatusCodeError):
    pass


class MethodNotFoundError(Error):
    '''
        Returned when the RPC server of the Monero wallet is not able to understand the request
    '''
    pass
