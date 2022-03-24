import random
from abc import ABC
from pymongo import MongoClient

# https://pymongo.readthedocs.io/en/stable/index.html

client = MongoClient('mongodb://root:s3cr37@localhost:27017')
db = client.mydb


class ResultList(list):
    def first_or_none(self):
        return self[0] if len(self) > 0 else None


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

class Person(Document):
    # To specify which collection to store in.
    # In this case we store Person objects in the user collection.
    collection = db.users


class Product(Document):
    collection = db.products


def main():
    # strings = ['AA', 'BB', 'CC']
    #result = '\n'.join(s for s in strings)
    #print(result)

    user = {
        "first_name": "Petronella",
        "last_name": "Karlsson",
        "phone_numbers": ["55323435", "23453645432"],
        "address": {
            "street_address": "LångtbortIStan",
            "zip_code": "420 69",
            "city": "Mora"
        },
        "age": "44"
    }

    product_dict = [
        {
            'name': 'Ball',
            'price': 3.45
        },
        {
            'name': 'Car',
            'price': 420.69
        }
    ]

    # TODO: Create This method
    # Product.insert_many(product_dict)
    #new_user = Person(user)
    #Person.save(new_user)
    #get_user = Person.find(last_name='Petterson').first_or_none()
    #Person.delete(get_user)

    first_names = ['Alice', 'Bob', 'Carl', 'Dina', 'Erik', 'Frida', 'Gunnar']
    last_names = ['Andersson', 'Bengtsson' 'Carlsson', 'Danielsson', 'Eriksson', 'Fredriksson', 'Goransson']

    for _ in range(10):
        user['first_name'] = random.choice(first_names)
        user['last_name'] = random.choice(last_names)

    Person(user).save()
    #Person.delete_many(last_name='Svensson')

    ###########################

#    terje = Person.find(first_name='Vice').first_or_none()
#    print(terje)
#    terje.first_name = 'Terje'
#    terje.save()

#    terje = Person.find(first_name='Terje').first_or_none()
#    print(terje)
#    print()
    print()

if __name__ == '__main__':
    main()
