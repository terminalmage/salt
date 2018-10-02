# -*- coding: utf-8 -*-
'''
This is the default pillar PCRE matcher.
'''
from __future__ import absolute_import, print_function, unicode_literals

import logging
from salt.defaults import DEFAULT_TARGET_DELIM  # pylint: disable=3rd-party-module-not-gated
import salt.utils.data  # pylint: disable=3rd-party-module-not-gated

log = logging.getLogger(__name__)

__virtualname__ = 'pillar_pcre'


def match(tgt, delimiter=DEFAULT_TARGET_DELIM):
    '''
    Matches the value of a Pillar key using a PCRE
    '''
    log.debug('pillar PCRE target: %s', tgt)
    if delimiter not in tgt:
        log.error('Got insufficient arguments for pillar PCRE match '
                  'statement from master')
        return False
    return salt.utils.data.subdict_match(
        __opts__['pillar'], tgt, delimiter=delimiter, regex_match=True
    )
