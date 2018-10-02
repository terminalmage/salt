# -*- coding: utf-8 -*-
'''
This is the default list matcher.
'''
from __future__ import absolute_import, print_function, unicode_literals
import logging

log = logging.getLogger(__name__)

__virtualname__ = 'list'


def match(tgt):
    '''
    Matches the Minion ID from a comma-separated list of IDs
    '''
    try:
        if ',' + __opts__['id'] + ',' in tgt \
                or tgt.startswith(__opts__['id'] + ',') \
                or tgt.endswith(',' + __opts__['id']):
            return True
        # tgt is a string, which we know because the if statement above did not
        # cause one of the exceptions being caught. Therefore, look for an
        # exact match. (e.g. salt -L foo test.ping)
        return __opts__['id'] == tgt
    except (AttributeError, TypeError):
        # tgt is not a string, maybe it's a sequence type?
        try:
            return __opts__['id'] in tgt
        except Exception:
            # tgt was likely some invalid type
            return False

    # We should never get here based on the return statements in the logic
    # above. If we do, it is because something above changed, and should be
    # considered as a bug. Log a warning to help us catch this.
    log.warning(
        'List matcher unexpectedly did not return, for target %s, '
        'this is probably a bug.', tgt
    )
    return False
