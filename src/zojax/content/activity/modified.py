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
from zope.lifecycleevent import Attributes
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.activity.interfaces import IActivity, IActivityAware
from zojax.activity.interfaces import IActivityRecordDescription
from zojax.content.type.interfaces import IContent, IContentType, IPortalType

from record import ContentActivityRecord
from interfaces import _, IContentModifiedRecord


class ContentModifiedRecord(ContentActivityRecord):
    interface.implementsOnly(IContentModifiedRecord)

    type = 'modified'
    verb = _('Modified')

    attributes = ()


class ContentModifiedRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = _('Modified')
    description = _('Content object has been modified.')


@component.adapter(IActivityAware, IObjectModifiedEvent)
def contentModifiedHandler(content, ev):
    if not ev.descriptions:
        return

    ct = IContentType(content, None)
    if ct is None:
        return

    activity = getUtility(IActivity)
    records = activity.objectRecords(content)

    record = IContentModifiedRecord(content)

    if records and IContentModifiedRecord.providedBy(records[0]) and \
            (records[0].principal == record.principal):
        oldRecord = records[0]
        activity.remove(oldRecord.id)

        attributes = dict([(attr.interface, list(attr.attributes)) \
                               for attr in ev.descriptions])

        for attr in oldRecord.attributes:
            data = attributes.get(attr.interface, [])
            if data:
                data = list(data[0])

            for attrs in attr.attributes:
                if isinstance(attrs, basestring):
                    if attrs not in data:
                        data.append(attrs)
                else:
                    for name in attrs:
                        if name not in data:
                            data.append(name)

            attributes[attr.interface] = tuple(data)

        attributes = [Attributes(iface, *data)
                      for iface, data in attributes.items()]

        record.attributes = tuple(attributes)
    else:
        record.attributes = ev.descriptions

    activity.add(content, record)
