from abc import ABCMeta
import zope
from zope import interface
from CrudService import CrudService


class AbstractCrudService(object):
    __metaclass__ = ABCMeta
    zope.interface.implements(CrudService)

    # TODO: implement CRUD functional
    # TODO: do we need this abstraction for CRUD or we can just take it from existing module?
