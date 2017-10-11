"""
    The ``exceptions`` module
    =============================
 
    Exceptions raised by PyMoneroWallet.
 
"""

class Error(Exception):
    "General PyMoneroWallet exception"
    pass


class HTTPStatusCodeError(Error):
    "HTTP status code is different from 200"
    pass


class Unauthorized(HTTPStatusCodeError):
    "HTTP status code 401 Unauthorized"
    pass


class RPCError(Error):
    "RPC error returned by the wallet"
    pass


class MethodNotFoundError(RPCError):
    "The RPC server of the Monero wallet is not able to understand the request"
    pass


# The following errors are based on
# https://github.com/monero-project/monero/blob/master/src/wallet/wallet_rpc_server_error_codes.h

class UnknownError(RPCError):
    pass

class WrongAddress(RPCError):
    pass

class DaemonIsBusy(RPCError):
    pass

class GenericTransferError(RPCError):
    "Error performing an XMR transaction"
    pass

class WrongPaymentID(RPCError):
    pass

class WrongTransferType(RPCError):
    pass

class Denied(RPCError):
    pass

class WrongTransactionID(RPCError):
    pass

class WrongSignature(RPCError):
    pass

class WrongKeyImage(RPCError):
    pass

class WrongURI(RPCError):
    pass

class WrongIndex(RPCError):
    pass

class WalletNotOpen(RPCError):
    pass

class TransactionTooLarge(RPCError):
    pass

class NotEnoughMoney(RPCError):
    pass

class NotEnoughOutputsToMix(RPCError):
    pass

class ZeroDestination(RPCError):
    pass

class TransactionNotPossible(RPCError):
    pass

class WalletAlreadyExists(RPCError):
    pass

class InvalidPassword(RPCError):
    pass

class NoWalletDirConfigured(RPCError):
    pass

_errorcode_to_exception = {
     -1 : UnknownError,
     -2 : WrongAddress,
     -3 : DaemonIsBusy,
     -4 : GenericTransferError,
     -5 : WrongPaymentID,
     -6 : WrongTransferType,
     -7 : Denied,
     -8 : WrongTransactionID,
     -9 : WrongSignature,
    -10 : WrongKeyImage,
    -11 : WrongURI,
    -12 : WrongIndex,
    -13 : WalletNotOpen,
# Proposal (https://github.com/monero-project/monero/pull/2619)
    -14 : TransactionTooLarge,
    -15 : NotEnoughMoney,
    -16 : NotEnoughOutputsToMix,
    -17 : ZeroDestination,
    -18 : TransactionNotPossible,
    -19 : WalletAlreadyExists,
    -20 : InvalidPassword,
    -21 : NoWalletDirConfigured,
}
