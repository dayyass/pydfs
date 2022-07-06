import zope
from zope import interface


class CrudService(zope.interface.Interface):
    your_attribute = zope.interface.Attribute("""...""")
    # TODO: is it good idea to use interfaces in python?
