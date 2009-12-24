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
""" zojax.content.actions tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component, event
from zope.app.testing import functional, setup, placelesssetup
from zope.app.component.hooks import setSite
from zope.app.rotterdam import Rotterdam
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.security.interfaces import IAuthentication
from zope.lifecycleevent import ObjectCreatedEvent
from zojax.cache.testing import setUpCache, tearDownCache
from zojax.activity.interfaces import IActivity, IActivityAware
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.ownership.interfaces import IOwnership
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.personal.space.manager import \
    PersonalSpaceManager, IPersonalSpaceManager

zojaxContentActivityLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxContentActivityLayer', allow_teardown=True)


class IContent(IItem):
    pass


class Content(PersistentItem):
    interface.implements(IContent)


class Content2(PersistentItem):
    interface.implements(IActivityAware)


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxContentActivityLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        root = functional.getRootFolder()
        setSite(root)
        setUpCache()

        sm = root.getSiteManager()

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # catalog
        root['catalog'] = Catalog()
        sm.registerUtility(root['catalog'], ICatalog)

        # people
        root['people'] = PersonalSpaceManager()
        sm.registerUtility(root['people'], IPersonalSpaceManager)

        user = sm.getUtility(IAuthentication).getPrincipal('zope.mgr')
        root['people'].assignPersonalSpace(user)

        activity = sm.getUtility(IActivity)
        try:
            activity.remove(activity.records.keys()[0])
        except IndexError:
            pass


    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        tearDownCache()
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("testbrowser.txt"),
            ))
