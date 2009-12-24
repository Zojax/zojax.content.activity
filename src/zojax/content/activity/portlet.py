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
from zope import interface
from zope.component import getUtility
from zope.app.component.hooks import getSite
from zojax.layout.interfaces import ILayout
from zojax.activity.interfaces import IActivity
from zojax.content.type.interfaces import IContent

from zojax.cache.view import cache
from zojax.cache.keys import VisibleContext
from zojax.cache.timekey import TagTimeKey, each30minutes
from zojax.portlet.cache import PortletModificationTag

from cache import ActivityTag
from interfaces import IActivityPortlet


class ActivityPortlet(object):
    interface.implements(IActivityPortlet)

    def __init__(self, context, request, manager, view):
        view = getattr(manager, 'view', None)
        if ILayout.providedBy(view):
            context = view.maincontext

        context = context or getSite()

        super(ActivityPortlet, self).__init__(context, request, manager, view)

    def listContents(self):
        query = {'contexts': (self.context,)}
        if self.types:
            query['type'] = {'any_of': self.types}

        return [
            record for record in getUtility(
                IActivity).search(**query)[:self.number]]

    @cache('portlet.activity', VisibleContext, PortletModificationTag,
           TagTimeKey(ActivityTag, each30minutes))
    def updateAndRender(self):
        return super(ActivityPortlet, self).updateAndRender()
