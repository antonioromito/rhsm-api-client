# Copyright (C) 2019 Antonio Romito (aromito@redhat.com)
#
# This file is part of the sos project: https://github.com/aromito/rhsm-api-client
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.
import gettext

__version__ = "1.0"

gettext_dir = "/usr/share/locale"
gettext_app = "rhsm-api-client"

gettext.bindtextdomain(gettext_app, gettext_dir)

def _default(msg):
    return gettext.dgettext(gettext_app, msg)


_rhsm = _default
