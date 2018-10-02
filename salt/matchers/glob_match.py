# -*- coding: utf-8 -*-
'''
This is the default glob matcher function.
'''
from __future__ import absolute_import, print_function, unicode_literals

import fnmatch
from salt.ext import six  # pylint: disable=3rd-party-module-not-gated

__virtualname__ = 'glob'


def match(tgt):
    '''
    Matches a Minion ID using globbing
    '''
    if not isinstance(tgt, six.string_types):
        return False

    return fnmatch.fnmatch(__opts__['id'], tgt)
