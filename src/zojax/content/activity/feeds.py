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
import time, rfc822
from zope import interface, component
from zope.component import getUtility, queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IAuthentication

from zojax.content.feeds.rss2 import RSS2Feed
from zojax.content.type.interfaces import IContentViewView
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.activity.interfaces import IActivity, IActivityAware

from interfaces import _, IActivityRSSFeed


class ActivityRSSFeed(RSS2Feed):
    component.adapts(IActivityAware)
    interface.implementsOnly(IActivityRSSFeed)

    name = u'activity'
    title = _(u'Recent activity')
    description = _(u'Content recent activity.')

    def items(self):
        request = self.request
        types = {}

        for record in getUtility(IActivity).search(
            contexts = (self.context,))[:50]:

            content = record.object

            view = queryMultiAdapter((content, request), IContentViewView)
            try:
                if view is not None:
                    url = '%s/%s'%(absoluteURL(content, request), view.name)
                else:
                    url = '%s/'%absoluteURL(content, request)
            except:
                continue

            if record.type not in types:
                types[record.type] = record.description

            type = types.get(record.type, record.type) or record.type
            if type is not None:
                title = type.title
            else:
                title = _('Unknown')

            info = {
                'title': title,
                'link': '%s'%url,
                'guid': str(record.date),
                'pubDate': rfc822.formatdate(time.mktime(record.date.timetuple())),
                'description': u'',
                'isPermaLink': True}

            auth = getUtility(IAuthentication)
            try:
                principal = auth.getPrincipal(record.principal)
            except:
                principal = None

            if principal is not None:
                profile = IPersonalProfile(principal)
                author = profile.title
                info['author'] = u'%s (%s)'%(profile.email, author)

                info['description'] = u'by %s '%author

            info['description'] += 'on %s'%getattr(
                content, 'title', getattr(content, '__name__', u''))

            yield info
