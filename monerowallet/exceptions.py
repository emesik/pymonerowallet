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


class HTTPStatusCodeError(Error):
    '''
        Returned when HTTP status code is different from 200
    '''
    pass


class Unauthorized(HTTPStatusCodeError):
    pass


class RPCError(Error):
    '''
        RPC error returned by the wallet
    '''
    pass


class MethodNotFoundError(RPCError):
    '''
        Returned when the RPC server of the Monero wallet is not able to understand the request
    '''
    pass


class GenericTransferError(RPCError):
    pass
