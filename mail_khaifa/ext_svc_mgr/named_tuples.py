'''
Used instead of trivial interfaces
'''
import collections

#State Transition for Notification
StateTransition=collections.namedtuple('StateTransition', ('external_id', 'updated_state'))

#result of 3rd party API call
ExtClientResult=collections.namedtuple('ExtClientResult', ('external_id', 'is_success', 'failure_reason'))

