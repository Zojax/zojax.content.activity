##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope.component import getUtility, queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IAuthentication

from zojax.formatter.utils import getFormatter
from zojax.content.type.interfaces import IContentViewView
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.content.activity.interfaces import _


class PortletRecordView(object):

    avatar = u''
    profile = u''

    def update(self):
        record = self.context
        request = self.request

        content = record.object
        formatter = getFormatter(request, 'humanDatetime', 'medium')

        view = queryMultiAdapter((content, request), IContentViewView)
        try:
            if view is not None:
                url = '%s/%s'%(absoluteURL(content, request), view.name)
            else:
                url = '%s/'%absoluteURL(content, request)
        except:
            url = u''

        self.url = url
        self.title = getattr(content, 'title', content.__name__)
        self.description = getattr(content, 'description', u'')
        self.date = formatter.format(record.date)
        self.content = content

        auth = getUtility(IAuthentication)
        try:
            principal = auth.getPrincipal(record.principal)
        except:
            principal = None

        if principal is not None:
            profile = IPersonalProfile(principal)
            self.avatar = profile.avatarUrl(request)
            self.author = profile.title

            space = profile.space
            if space is not None:
                self.profile = '%s/'%absoluteURL(space, request)
        else:
            self.author = _('Unknown')
