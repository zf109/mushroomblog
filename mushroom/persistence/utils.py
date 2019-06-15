from abc import abstractclassmethod
from urllib.parse import urlparse
import json

class Saveable(object):
    """
        pattern for savable mixin
    """
    def saves(self):
        return {
            'class': '.'.join([self.__class__.__module__, self.__class__.__name__]),
            'params': self.to_dict()
        }

    def save(self, filepath):
        with open(filepath, "w") as f:
            savejson = self.saves()
            json.dump(savejson, f)

    @classmethod
    def loads(cls, serialised, *args, **kwargs):
        class_ = serialised.get('class')
        class_fullname = '.'.join([cls.__module__, cls.__name__])
        if class_ != class_fullname:
            raise TypeError(f'Expecting class {class_fullname}, but got {class_}')
        return cls.from_dict(serialised, *args, **kwargs)

    @classmethod
    def load(cls, urlstring, *args, **kwargs):
        """
            load function can load by given an url string. By default it will load from file:// scheme
            but can also be other such as s3:// etc.
        """
        locator = urlparse(urlstring)
        if not (locator.scheme or locator.hostname):
            with open(locator.path, "r") as f:
                serialised = json.load(f)
            return cls.loads(serialised)

    def to_dict(self):
        raise NotImplementedError()

    @abstractclassmethod
    def from_dict(self, serialised):
        raise NotImplementedError()
