from graphene import Enum

class Registry(object):
    def __init__(self):
        self._registry = {}
        self._registry_enum = {}

    def register(self, cls):
        from .types import MongoengineObjectType

        assert issubclass(
            cls, MongoengineObjectType
        ), 'Only MongoengineObjectTypes can be registered, received "{}"'.format(
            cls.__name__
        )
        assert cls._meta.registry == self, "Registry for a Model have to match."
        self._registry[cls._meta.model] = cls

        # Rescan all fields
        for model, cls in self._registry.items():
            cls.rescan_fields()

    def get_type_for_model(self, model):
        return self._registry.get(model)

    def register_enum(self, cls):
        from enum import EnumMeta
        assert type(cls) == EnumMeta, 'Only EnumMeta can be registered, received "{}"'.format(cls.__name__)
        self._registry_enum[cls] = Enum.from_enum(cls)

    def check_enum_already_exist(self, cls):
        return cls in self._registry_enum

    def get_type_for_enum(self, cls):
        return self._registry_enum.get(cls)


registry = None


def get_global_registry():
    global registry
    if not registry:
        registry = Registry()
    return registry


def reset_global_registry():
    global registry
    registry = None
