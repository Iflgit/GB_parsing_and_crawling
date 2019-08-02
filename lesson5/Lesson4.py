from pymongo import MongoClient
import pprint

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['lesson']
lesson = db.lesson  # Имя коллекции
lesson.drop()
lesson.insert_many([{'name': "test abc",
                   'size': 2000,
                    'author': "Mike Dowson"},
                    {'name': "Name space",
                     'size': 1500,
                    'author': "Peter Pan"}
                     ])
print(lesson.count_documents({}))

doc_data = {
     "name": "One more document",
     "author": {
             "fullname": "Sergie",
             "age": 18,
            "address":
                {'street': "Иванова",
                 'city': 'Москва'}
     },
     "created": "01.12.1982",
"genres": ["философия", "action", "psy"]
}
lesson.insert_one(doc_data)

pprint.pprint(lesson.find_one({'author.address.city': 'Москва'}))
