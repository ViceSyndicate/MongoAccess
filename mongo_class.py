from abc import ABC
from pymongo import MongoClient

# https://pymongo.readthedocs.io/en/stable/index.html

client = MongoClient('mongodb://root:s3cr37@localhost:27017')
db = client.mydb


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
        self.collection.insert_one(self.__dict__)


class Person(Document):
    # To specify which collection to store in.
    # In this case we store Person objects in the user collection.
    collection = db.users


def main():
    # strings = ['AA', 'BB', 'CC']
    #result = '\n'.join(s for s in strings)
    #print(result)

    user = {
        "first_name": "Stina",
        "last_name": "Bengtsson",
        "phone_numbers": ["55323435", "23453645432"],
        "address": {
            "street_address": "Lilgatan 2",
            "zip_code": "543 21",
            "city": "Lilstan"
        }
    }

    #k is key like PrimaryKey, v is the value connected to the key.
    #result = '\n'.join(f'{k} = {v}' for k, v in user.items())
    #print(result)

    person = Person(user)
    person.save()
    print(person)

if __name__ == '__main__':
    main()
