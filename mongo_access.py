from abc import ABC
from pymongo import MongoClient

client = MongoClient('mongodb://root:s3cr37@localhost:27017')
db = client.mydb


class ResultList(list):
    def first_or_none(self):
        return self[0] if len(self) > 0 else None

    def last_or_none(self):
        return self[-1] if len(self) > 0 else None


class Document(ABC):
    collection = None

    def __init__(self, data):
        # Set the objects variables to the objects.__dict__ values.
        # All objects have a .__dict__ value.
        self.__dict__ = data

    def __repr__(self):
        # .items() is tuples that we use to iterate through with our keys and values.
        return '\n'.join(f'{k} = {v}' for k, v in self.__dict__.items())

    def save(self):
        if '_id' not in self.__dict__:
            self.collection.insert_one(self.__dict__)
        else:
            self.collection.replace_one({'_id': self._id}, self.__dict__)

    def delete(self):
        self.collection.delete_one(self.__dict__)

    #cls is used to get current sub-class
    @classmethod
    def save_many(cls, items):
        for item in items:
            cls(item).save()

    @classmethod
    def delete_many(cls, **kwargs):
        cls.collection.delete_many(kwargs)

    # Classmethod is needed for cls to work I think...
    @classmethod
    def all(cls):
        # cls is class type
        # so return list [Class(item) for item in Class.collection.find()]
        return [cls(item) for item in cls.collection.find()]

    @classmethod
    def find(cls, **kwargs):
        return ResultList(cls(item) for item in cls.collection.find(kwargs))

    def delete_field(self, field):
        self.collection.update_one({'_id': self._id}, {"$unset": {field: ""}})
