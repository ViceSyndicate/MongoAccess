from pymongo import MongoClient

client = MongoClient('mongodb://root:s3cr37@localhost:27017')
db = client.testing


def add_user():
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

    db.users.insert_one(user)


def main():

    add_user()

    users = db.users.find({'last_name': 'Bengtsson'})
    for user in users:
        print(user)


if __name__ == '__main__':
    main()


