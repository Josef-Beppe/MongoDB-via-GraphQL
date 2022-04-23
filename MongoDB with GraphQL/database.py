import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from random_data import getFullRndDoc

client = AsyncIOMotorClient('localhost', 27017)
# Test if its connected, or maybe after db = client...
db = client['test_database']

''' ***** Start of functions for schema.py ***** '''

''' Fills database with sample data '''
async def do_insert_random():
    result = await db.test_collection.insert_many(
        [getFullRndDoc() for i in range(5)])

''' Prints whole database into command line '''
async def print_all():
    c = db.test_collection
    async for document in c.find({}):
        print(document)
        print("\n")

''' Returns the first found document with 'name' '''
async def do_find_one(name):
    document = await db.test_collection.find_one({'name': name})
    return document

''' Returns a list of dictionaries (documents) '''
async def do_find(name):
    cursor = db.test_collection.find({'name': name})
    documents = await cursor.to_list(length=100)
    return documents

''' ***** End of functions for schema.py ***** '''
''' ***** Start of functions for models.py ***** '''

''' Writes dictionary into database '''
async def do_insert(dictionary):
    document = dictionary
    result = await db.test_collection.insert_one(document)
    return result

async def do_update(original, new):
    coll = db.test_collection
    result = await coll.update_one(original, {'$set': new})
    new_document = await coll.find_one(new)
    print('document is now %s' % new_document)
    return new_document

async def do_delete_many(dictionary):
    coll = db.test_collection
    n = await coll.count_documents({})
    print('%s documents before calling delete_many()' % n)
    result = await db.test_collection.delete_many(dictionary)
    print('%s documents after' % (await coll.count_documents({})))
    return 0

''' ***** End of functions for models.py ***** '''

def init_db():
	collection = db['test_collection']
	db.test_collection.delete_many({}) # Clear the collection at start