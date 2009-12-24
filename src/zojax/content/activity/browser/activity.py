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
from zope.component import getUtility, queryMultiAdapter
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from zojax.table.table import Table
from zojax.table.column import Column, AttributeColumn
from zojax.formatter.utils import getFormatter
from zojax.activity.interfaces import IActivity, IActivityAware
from zojax.content.table.author import AuthorNameColumn
from zojax.content.activity.interfaces import IActivityRecordDescriptionView

from interfaces import _, IActivityTable


class ActivityTable(Table):
    interface.implements(IActivityTable)
    component.adapts(IActivityAware, interface.Interface, interface.Interface)

    title = _('Activity')

    pageSize = 10
    enabledColumns = ('type', 'author', 'date', 'description')
    msgEmptyTable = _('No activity.')
    cssClass = 'z-table z-content-activity'

    def initDataset(self):
        self.dataset = getUtility(IActivity).objectRecords(self.context)


class TypeColumn(AttributeColumn):
    component.adapts(interface.Interface, interface.Interface, IActivityTable)

    name = 'type'
    title = _('Type')
    cssClass = 'ctb-activity-type'

    def update(self):
        super(TypeColumn, self).update()

        self.table.environ['recordTypes'] = {}

    def query(self):
        type = self.content.type
        types = self.globalenviron['recordTypes']

        if type not in types:
            types[type] = self.content.description

        tp = types.get(type)
        if tp is not None:
            return tp.title
        else:
            return _('Unknown')


class AuthorColumn(AuthorNameColumn):
    component.adapts(interface.Interface, interface.Interface, IActivityTable)

    title = _('Member')

    def getPrincipal(self, content):
        try:
            if self.content.principal:
                return getUtility(
                    IAuthentication).getPrincipal(self.content.principal)
        except PrincipalLookupError:
            return None


class DateColumn(AttributeColumn):
    component.adapts(interface.Interface, interface.Interface, IActivityTable)

    name = 'date'
    title = _('Date')
    cssClass = 'ctb-activity-date'
    attrName = 'date'

    def update(self):
        super(DateColumn, self).update()

        self.table.environ['fancyDatetime'] = getFormatter(
            self.request, 'fancyDatetime', 'medium')

    def render(self):
        value = self.query()
        if value:
            return self.globalenviron['fancyDatetime'].format(value)

        return u'---'


class DescriptionColumn(Column):
    component.adapts(interface.Interface, interface.Interface, IActivityTable)

    name = 'description'
    title = _('Description')
    cssClass = 'ctb-activity-desc'

    def render(self):
        view = queryMultiAdapter(
            (self.content, self.request), IActivityRecordDescriptionView)

        if view is not None:
            view.update()
            return view.render()

        return u''
