import zope
from zope import interface
from crud.AbstractCrudService import AbstractCrudService
from SlaveService import SlaveService


class SlaveServiceImpl(AbstractCrudService):
    zope.interface.implements(SlaveService)
