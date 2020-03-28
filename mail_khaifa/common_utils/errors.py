import collections

class Error(object):
    __slots__=[]

    ErrorInfo = collections.namedtuple('ErrorInfo', ('code', 'message'))

    NO_ERROR=ErrorInfo(0, None)
    INVALID_PARAMETERS=ErrorInfo(1, 'Invalid Parameters')
    UNKNOWN_ERROR=ErrorInfo(999, 'Unknown Error')
