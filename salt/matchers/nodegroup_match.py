# -*- coding: utf-8 -*-
'''
This is the default nodegroup matcher.
'''
from __future__ import absolute_import, print_function, unicode_literals

import salt.utils.minions   # pylint: disable=3rd-party-module-not-gated
import salt.loader

__virtualname__ = 'nodegroup'

# NOTE: This is a compatibility matcher and is NOT called when using nodegroups
# for remote execution, but is called when the nodegroups matcher is used in
# states


def match(tgt, nodegroups):
    '''
    Matches using compound match expressions defined as nodegroups
    '''
    if tgt in nodegroups:
        matchers = salt.loader.matchers(__opts__)
        return matchers['compound.match'](
            salt.utils.minions.nodegroup_comp(tgt, nodegroups)
        )
    return False
