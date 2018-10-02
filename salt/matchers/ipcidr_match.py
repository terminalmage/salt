# -*- coding: utf-8 -*-
'''
This is the default ipcidr matcher.
'''
from __future__ import absolute_import, print_function, unicode_literals

import logging
from salt.ext import six  # pylint: disable=3rd-party-module-not-gated

import salt.utils.network  # pylint: disable=3rd-party-module-not-gated

if six.PY3:
    import ipaddress
else:
    import salt.ext.ipaddress as ipaddress

log = logging.getLogger(__name__)

__virtualname__ = 'ipcidr'
__virtual_aliases__ = ('subnet',)


def match(tgt):
    '''
    Matches based on IP address or CIDR notation (i.e. subnet membership)
    '''
    try:
        # Target is an address?
        tgt = ipaddress.ip_address(tgt)
    except:  # pylint: disable=bare-except
        try:
            # Target is a network?
            tgt = ipaddress.ip_network(tgt)
        except:  # pylint: disable=bare-except
            log.error('Invalid IP/CIDR target: %s', tgt)
            return []
    proto = 'ipv{0}'.format(tgt.version)

    grains = __opts__['grains']

    if proto not in grains:
        match = False
    elif isinstance(tgt, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        match = six.text_type(tgt) in grains[proto]
    else:
        match = salt.utils.network.in_subnet(tgt, grains[proto])

    return match
