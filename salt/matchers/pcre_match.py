# -*- coding: utf-8 -*-
'''
This is the default pcre matcher.
'''
from __future__ import absolute_import, print_function, unicode_literals

import re

__virtualname__ = 'pcre'


def match(tgt):
    '''
    Matches the minion ID using a Perl-compatible regular expression (PCRE)
    '''
    return bool(re.match(tgt, __opts__['id']))
