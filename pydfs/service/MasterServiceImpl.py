import zope
from zope import interface
from crud.AbstractCrudService import AbstractCrudService
from MasterService import MasterService


class MasterServiceImpl(AbstractCrudService):
    zope.interface.implements(MasterService)
