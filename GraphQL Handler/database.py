import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongo', 27017)
# Test if its connected, or maybe after db = client...
db = client['test_database']

loop = asyncio.get_event_loop()
''' ***** Start of functions for schema.py ***** '''

''' Fills database with sample data '''
async def do_insert_defaultdata():
    
    data=[
        {"id":"1", "name":"Timmy", "surname":"Trumpet", "age":"35", "memberships":[["11","31"],["13","32"],["15","31"]]},
        {"id":"2", "name":"Ava", "surname":"Max", "age":"25", "memberships":[["11","31"],["16","31"]]},
        {"id":"3", "name":"Becky", "surname":"Hill", "age":"30", "memberships":[["11","32"],["13","31"]]},
        {"id":"4", "name":"Dua", "surname":"Lipa", "age":"28", "memberships":[["11","31"],["14","33"]]},
        {"id":"5", "name":"Jan", "surname":"Veliky", "age":"60", "memberships":[["15","31"]]},  
        {"id":"6", "name":"Petr", "surname":"Maly", "age":"25", "memberships":[["15","32"]]},
        {"id":"7", "name":"Pavel", "surname":"Novotny", "age":"42", "memberships":[["15","31"]]},
        {"id":"8", "name":"David", "surname":"Guetta", "age":"40", "memberships":[["12","32"]]},

        {"id":"11", "name":"FVT", "groupType":"21", "members":["1","2","3","4"]},
        {"id":"12", "name":"FVL", "groupType":"21", "members":["8"]},
        {"id":"13", "name":"23-5KB", "groupType":"23", "members":["1","3"]},
        {"id":"14", "name":"21-5TPVO", "groupType":"23", "members":["4"]},
        {"id":"15", "name":"Katedra informatiky a kybernetickych operaci", "groupType":"22", "members":["1","5","6","7"]},
        {"id":"16", "name":"Katedra radiolokace", "groupType":"22", "members":["2"]},
        
        {"id":"21", "name":"fakulta"},
        {"id":"22", "name":"katedra"},
        {"id":"23", "name":"ucebni skupina"},
        
        {"id":"31", "name":"student"},
        {"id":"32", "name":"ucitel"},
        {"id":"33", "name":"vedouci katedry"}]

    for doc in data:
        result = await do_insert(doc)

    '''data_users_groups = [
        {"id":"1", "users_id":"1", "groups_id":"11", "roleType_id":"31"},
        {"id":"2", "users_id":"1", "groups_id":"13", "roleType_id":"32"},
        {"id":"3", "users_id":"1", "groups_id":"15", "roleType_id":"31"},

        {"id":"4", "users_id":"2", "groups_id":"11", "roleType_id":"31"},
        {"id":"5", "users_id":"2", "groups_id":"16", "roleType_id":"31"},

        {"id":"6", "users_id":"3", "groups_id":"11", "roleType_id":"32"},
        {"id":"7", "users_id":"3", "groups_id":"13", "roleType_id":"31"},

        {"id":"8", "users_id":"4", "groups_id":"11", "roleType_id":"31"},
        {"id":"9", "users_id":"4", "groups_id":"14", "roleType_id":"33"},

        {"id":"10", "users_id":"5", "groups_id":"15", "roleType_id":"31"},
        {"id":"11", "users_id":"6", "groups_id":"15", "roleType_id":"32"},
        {"id":"12", "users_id":"7", "groups_id":"15", "roleType_id":"31"},

        {"id":"13", "users_id":"8", "groups_id":"12", "roleType_id":"32"}
    ]'''
    
''' Prints whole database into command line '''
async def print_all():
    c = db.test_collection
    async for document in c.find({}):
        print(document)
        print("\n")

''' Returns the first found document with 'name' '''
'''async def do_find_one(name):
    document = await db.test_collection.find_one({'name': name})
    return document'''

async def do_find_id(id):
    document = await db.test_collection.find_one({'id': id})
    return document

''' Returns a list of dictionaries (documents) '''
'''async def do_find(name):
    cursor = db.test_collection.find({'name': name})
    documents = await cursor.to_list(length=100)
    return documents'''

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

g_id=0

def get_id():
    global g_id
    g_id=g_id+1
    return str(g_id)
