import zope
from zope import interface
from crud.CrudService import CrudService


class MasterService(zope.interface.Interface):
    # TODO: is it correct to inherit from CrudService?
    zope.interface.implements(CrudService)

    your_attribute = zope.interface.Attribute("""...""")
    # TODO: is it good idea to use interfaces in python?
