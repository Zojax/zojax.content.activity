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
from zope import interface, component
from zope.component import getUtility
from zope.app.container.interfaces import IObjectRemovedEvent

from zojax.activity.interfaces import IActivity, IActivityAware
from zojax.activity.interfaces import IActivityRecordDescription
from zojax.content.type.interfaces import IContent, IContentType, IPortalType

from record import ContentActivityRecord
from interfaces import _, IContentRemovedRecord


class ContentRemovedRecord(ContentActivityRecord):
    interface.implementsOnly(IContentRemovedRecord)

    type = 'removed'
    verb = _('Removed')
    objectType = None

    def __init__(self, content, **kw):
        super(ContentRemovedRecord, self).__init__(content, **kw)

        self.objectTitle = getattr(content, 'title', u'')
        self.objectType = IContentType(content).name


class ContentRemovedRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = _('Removed')
    description = _('Content object has been removed.')


@component.adapter(IActivityAware, IObjectRemovedEvent)
def contentRemovedHandler(content, ev):
    parent = ev.oldParent
    if not IActivityAware.providedBy(parent):
        return

    getUtility(IActivity).add(parent, IContentRemovedRecord(content))
