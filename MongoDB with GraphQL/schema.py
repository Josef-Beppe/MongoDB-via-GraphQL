from graphene import ObjectType, Schema, String, Int, Field, List
from database import do_insert_random, print_all, do_find_one, do_find
import asyncio
from models import User, UserCreate, UserUpdate, UserDelete

loop = asyncio.get_event_loop()

''' Class for making changes in database '''
class Mutation(ObjectType):
	user_create = UserCreate.Field()
	user_update = UserUpdate.Field()
	user_delete = UserDelete.Field()

''' For searching and displaying data '''
class Query(ObjectType):
	fill_db = String()
	user = Field(User, name=String(required=True))
	user_all = List(User, name=String(required=True))
	user2 = String(name=String())

	''' Resolvers perform action, when the above is called '''
	def resolve_fill_db(root, info):
		loop.run_until_complete(do_insert_random())
		loop.run_until_complete(print_all())
		return "Filled"

	def resolve_user(root, info, name):
		return loop.run_until_complete(do_find_one(name))

	def resolve_user_all(root, info, name):
		return loop.run_until_complete(do_find(name))

	def resolve_user2(root, info, name):
		return loop.run_until_complete(do_find_one(name))


schema = Schema(query=Query, mutation=Mutation)