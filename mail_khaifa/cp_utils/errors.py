import collections

ErrorInfo = collections.namedtuple('ErrorInfo', ('code', 'message'))

class CpError(object):
    NO_ERROR=ErrorInfo(0, None)
    INVALID_PARAMETERS=ErrorInfo(1, 'Invalid Parameters')
