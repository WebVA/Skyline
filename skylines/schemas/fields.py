from marshmallow.fields import *  # NOQA
from marshmallow.fields import String as _String


class String(_String):
    def __init__(self, strip=False, *args, **kwargs):
        super(String, self).__init__(*args, **kwargs)
        self.strip = strip

    def _deserialize(self, value, attr, data):
        value = super(String, self)._deserialize(value, attr, data)

        if self.strip:
            value = value.strip()

        return value


# Aliases
Str = String
