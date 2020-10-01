# -*- coding: utf-8 -*-
"""
Configuration of the kernel using sysctl
========================================

Control the kernel sysctl system.

.. code-block:: yaml

  vm.swappiness:
    sysctl.present:
      - value: 20
"""
from __future__ import absolute_import, print_function, unicode_literals

# Import python libs
import re

# Import salt libs
from salt.exceptions import CommandExecutionError

# Import 3rd part libs
from salt.ext import six


def __virtual__():
    """
    This state is only available on Minions which support sysctl
    """
    if "sysctl.show" in __salt__:
        return True
    return (False, "sysctl module could not be loaded")


def present(name, value, config=None, ignore=False):
    """
    Ensure that the named sysctl value is set in memory and persisted to the
    named configuration file. The default sysctl configuration file is
    /etc/sysctl.conf

    name
        The name of the sysctl value to edit

    value
        The sysctl value to apply

    config
        The location of the sysctl configuration file. If not specified, the
        proper location will be detected based on platform.

    ignore
        .. versionadded:: 3001

        Adds --ignore to sysctl commands. This suppresses errors in environments
        where sysctl settings may have been disabled in kernel boot configuration.
        Defaults to False
    """
    ret = {"name": name, "result": True, "changes": {}, "comment": ""}

    if config is None:
        # Certain linux systems will ignore /etc/sysctl.conf, get the right
        # default configuration file.
        if "sysctl.default_config" in __salt__:
            config = __salt__["sysctl.default_config"]()
        else:
            config = "/etc/sysctl.conf"

    if __opts__["test"]:
        current = __salt__["sysctl.show"]()
        configured = __salt__["sysctl.show"](config_file=config)
        if configured is None:
            ret["result"] = None
            ret["comment"] = (
                "Sysctl option {0} might be changed, we failed to check "
                "config file at {1}. The file is either unreadable, or "
                "missing.".format(name, config)
            )
            return ret
        if name in current and name not in configured:
            if re.sub(" +|\t+", " ", current[name]) != re.sub(
                " +|\t+", " ", six.text_type(value)
            ):
                ret["result"] = None
                ret["comment"] = "Sysctl option {0} set to be changed to {1}".format(
                    name, value
                )
                return ret
            else:
                ret["result"] = None
                ret["comment"] = (
                    "Sysctl value is currently set on the running system but "
                    "not in a config file. Sysctl option {0} set to be "
                    "changed to {1} in config file.".format(name, value)
                )
                return ret
        elif name in configured and name not in current:
            ret["result"] = None
            ret["comment"] = (
                "Sysctl value {0} is present in configuration file but is not "
                "present in the running config. The value {0} is set to be "
                "changed to {1}".format(name, value)
            )
            return ret
        elif name in configured and name in current:
            if six.text_type(value).split() == __salt__["sysctl.get"](name).split():
                ret["result"] = True
                ret["comment"] = "Sysctl value {0} = {1} is already set".format(
                    name, value
                )
                return ret
        # otherwise, we don't have it set anywhere and need to set it
        ret["result"] = None
        ret["comment"] = "Sysctl option {0} would be changed to {1}".format(name, value)
        return ret

    try:
        update = __salt__["sysctl.persist"](name, value, config, ignore)
    except CommandExecutionError as exc:
        ret["result"] = False
        ret["comment"] = "Failed to set {0} to {1}: {2}".format(name, value, exc)
        return ret

    if update == "Updated":
        ret["changes"] = {name: value}
        ret["comment"] = "Updated sysctl value {0} = {1}".format(name, value)
    elif update == "Already set":
        ret["comment"] = "Sysctl value {0} = {1} is already set".format(name, value)
    elif update == "Ignored":
        ret["comment"] = "Sysctl value {0} = {1} was ignored".format(name, value)

    return ret
