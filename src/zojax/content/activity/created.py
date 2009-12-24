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
from zope.app.intid.interfaces import IIntIdAddedEvent

from zojax.activity.interfaces import IActivity, IActivityAware
from zojax.activity.interfaces import IActivityRecordDescription
from zojax.content.type.interfaces import IContentType, IPortalType

from record import ContentActivityRecord
from interfaces import _, IContentCreatedRecord


class ContentCreatedRecord(ContentActivityRecord):
    interface.implementsOnly(IContentCreatedRecord)

    score = 0.1
    type = 'created'
    verb = _('Created')


class ContentCreatedRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = _('Created')
    description = _('Content object has been created.')


@component.adapter(IActivityAware, IIntIdAddedEvent)
def contentCreatedHandler(content, ev):
    ct = IContentType(content, None)
    if ct is None:
        return

    getUtility(IActivity).add(content, IContentCreatedRecord(content))
