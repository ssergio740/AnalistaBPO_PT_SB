from pymongo import MongoClient
#iniciar mongodb "C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe" --dbpath="c:\data\db"
database= "mongodb+srv://sesierrag:lqJhgCcj7nqsEYOG@cvsierrainnovate.gyzkx.mongodb.net/"
cliente = MongoClient(database)
db=cliente["CVSierraInnovate"]
expedb = db.experience
user_db = db.users
edudb = db.education
referdb = db.references
lenguadb = db.lengua
skillsdb = db.skills
proyectdb = db.proyects
puestosdb = db.puestos