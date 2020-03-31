import collections

class Error(object):
    __slots__=[]

    ErrorInfo = collections.namedtuple('ErrorInfo', ('code', 'message'))

    NO_ERROR=ErrorInfo(0, None)
    INVALID_PARAMETERS=ErrorInfo(1, 'Invalid Parameters')
    INSUFFICIENT_PARAMETERS=ErrorInfo(2, 'Insufficient Parameters')
    CONSTRAINTS_NOT_POSSIBLE=ErrorInfo(3, 'Constraint cannot be met')
    EXTERNAL_ERROR=ErrorInfo(4, 'External Service Error')
    UNKNOWN_ERROR=ErrorInfo(999, 'Unknown Error')
