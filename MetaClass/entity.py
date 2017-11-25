import collections


def entity(cls):
    for key, attr in cls.__dict__.items():
        if isinstance(attr, collections.MutableMapping):
            type_name = type(attr).__name__
            attr.storage_name = '{}#{}'.format(type_name, key)
    return cls
