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

    # Classmethod is needed for cls to work I think...
    @classmethod
    def all(cls):
        # cls is class type
        # so return list [Class(item) for item in Class.collection.find()]
        return [cls(item) for item in cls.collection.find()]

    @classmethod
    def find(cls, **kwargs):
        return ResultList(cls(item) for item in cls.collection.find(kwargs))

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
        "last_name": "Petterson",
        "phone_numbers": ["55323435", "23453645432"],
        "address": {
            "street_address": "LångtbortIStan",
            "zip_code": "420 69",
            "city": "Mora"
        }
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
    new_user = Person(user)
    #Person.save(new_user)
    get_user = Person.find(last_name='Petterson').first_or_none()
    print(get_user)
    Person.delete(get_user)

    #person = Person.find(age=34).first_or_none()

    # Överkurs
    #if person:
        # TODO: Create this method
        # hint: db.collection.update_once({'_id': id}, {"$unset": {field: ""}})
        #person.delete_field('age')

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
