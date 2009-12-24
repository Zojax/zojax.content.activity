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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.widget.checkbox.field import CheckboxList
from zojax.activity.interfaces import IActivityRecord
from zojax.content.feeds.interfaces import IRSS2Feed

_ = MessageFactory('zojax.content.activity')


class IContentActivityRecord(IActivityRecord):
    """ content activity record """

    verb = interface.Attribute('activity verb')


class IContentCreatedRecord(IContentActivityRecord):
    """ content created """


class IContentModifiedRecord(IContentActivityRecord):
    """ content modified """

    attributes = interface.Attribute('Tuple of Attributes objects')


class IContentRemovedRecord(IContentActivityRecord):
    """ content removed """

    objectTitle = interface.Attribute('Removed object title')
    objectType = interface.Attribute('Removed object type')


class IActivityPortlet(interface.Interface):
    """ activity portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    types = CheckboxList(
        title = _(u'Types'),
        description = _(u'Select activity types. If none is selected, all types will be used.'),
        vocabulary = "acitivity.record.descriptions",
        default = [],
        required = False)

    number = schema.Int(
        title = _(u'Number of items'),
        description = _(u'Number of items to display'),
        default = 7,
        required = True)


class IActivityPortletRecordView(interface.Interface):
    """ record view for portlet """


class IActivityRecordDescriptionView(interface.Interface):
    """ record description view pagelet type """


class IActivityRSSFeed(IRSS2Feed):
    """ recent activity rss feed """
