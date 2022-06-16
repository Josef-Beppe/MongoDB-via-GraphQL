from graphene import ObjectType, Schema, String, Int, Field, List
from database import do_insert_defaultdata, print_all, do_find_one, do_find_id
import asyncio
from models import Person, PersonCreate, PersonUpdate, ItemDelete, Group, GroupCreate, GroupUpdate, AddPersonToGroup, RemovePersonFromGroup, RoleType, RoleTypeCreate, RoleTypeUpdate, GroupType, GroupTypeCreate, GroupTypeUpdate

loop = asyncio.get_event_loop()

''' Class for making changes in database '''
class Mutation(ObjectType):
	create_person = PersonCreate.Field()
	create_group = GroupCreate.Field()
	create_group_type = GroupTypeCreate.Field()
	create_role_type = RoleTypeCreate.Field()

	update_person = PersonUpdate.Field()
	update_group = GroupUpdate.Field()
	update_group_type = GroupTypeUpdate.Field()
	update_role_type = RoleTypeUpdate.Field()

	del_person = ItemDelete.Field()
	del_group = ItemDelete.Field()
	del_group_type = ItemDelete.Field()
	del_role_type = ItemDelete.Field()

	add_user_to_group = AddPersonToGroup.Field()
	remove_user_from_group = RemovePersonFromGroup.Field()


''' For searching and displaying data '''
class Query(ObjectType):
	fill_db = String()
	person = Field(Person, id=String(required=True))
	group = Field(Group, id=String(required=True))
	roleType = Field(RoleType, id = String(required = True))
	groupType = Field(GroupType, id = String(required = True))

	''' Resolvers perform action, when the above is called '''
	def resolve_fill_db(root, info):
		loop.run_until_complete(do_insert_defaultdata())
		loop.run_until_complete(print_all())
		return "Filled"

	def resolve_group(root, info, id):
		result = loop.run_until_complete(do_find_id(id))
		return result
		'''result = loop.run_until_complete(do_find_id(id))
		for i,personID in enumerate(result["members"]):
			result["members"][i] = loop.run_until_complete(do_find_id(personID))
			for x,groupID in enumerate(result["members"][i]["group"]):
				result["members"][i]["group"][x]=loop.run_until_complete(do_find_one(groupID))	
		return result'''

	def resolve_person(root, info, id):
		result = loop.run_until_complete(do_find_id(id))
		for i,groupID in enumerate(result["group"]):
			result["group"][i] = loop.run_until_complete(do_find_id(groupID))
			for x,personID in enumerate(result["group"][i]["members"]):
				result["group"][i]["members"][x]=loop.run_until_complete(do_find_one(personID))
		return result

	def resolve_roleType(root, info, id):
		return loop.run_until_complete(do_find_id(id))
	
	def resolve_groupType(root, info, id):
		return loop.run_until_complete(do_find_id(id))

	'''def resolve_person_all(root, info, name):
		return loop.run_until_complete(do_find(name))'''



schema = Schema(query=Query, mutation=Mutation)
