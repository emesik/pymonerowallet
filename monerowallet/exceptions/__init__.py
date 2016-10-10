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
        Returned exception when returned HTTP status code is different from 200
    '''
    pass

class MethodNotFoundError(Error):
    '''
        Returned exception when RCP server not able to understand the request
    '''
    pass
