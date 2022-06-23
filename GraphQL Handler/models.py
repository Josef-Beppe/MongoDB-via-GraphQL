from graphene import ObjectType, Mutation, String, Field, ID, List
from database import do_insert, do_update, do_delete_many, do_find_id, get_id
import asyncio
import copy

loop = asyncio.get_event_loop()

''' All that person can contain, graphql display '''
class Person(ObjectType):
    id= ID()
    name = String()
    surname = String()
    age = String()
    memberships = List(lambda: Membership)

    def resolve_memberships(parent, info):
        try:
            memberships=[]

            for mship in parent["memberships"]:
                membership=  Membership(
                    group = loop.run_until_complete(do_find_id(mship[0])),
                    roleType = loop.run_until_complete(do_find_id(mship[1])),
                )
                memberships.append(membership)
            return memberships
        except:
            memberships=[]
            for mship in parent.memberships:
                membership=  Membership(
                    group = loop.run_until_complete(do_find_id(mship[0])),
                    roleType = loop.run_until_complete(do_find_id(mship[1])),
                )
                memberships.append(membership)
            return memberships

class PersonCreate(Mutation):
    class Arguments:
        name = String()
        surname = String()
        age = String()

    person = Field(Person)
    
    def mutate(root, info, name=None, surname=None, age=None):
        person_data={
            'name':name,
            'surname':surname,
            'age':age,
            'id':get_id(),
            'memberships':[]
        }

        loop.run_until_complete(do_insert(person_data))
        print("Created")
        person = Person(
            id=person_data["id"],
            name=person_data["name"],
            surname=person_data["surname"],
            age=person_data["age"],
            memberships=person_data["memberships"]
        )
        return PersonCreate(person=person)

class PersonUpdate(Mutation):
    person = Field(Person)

    class Arguments:
        id = ID(required = True)
        name = String()
        surname = String()
        age = String()

    def mutate(parent, info, id, name=None, surname=None, age=None):
        person_data = loop.run_until_complete(do_find_id(id))
        person_dataNew=copy.deepcopy(person_data)
        if(type(name) == str): person_dataNew["name"] = name
        if(type(surname) == str): person_dataNew["surname"] = surname
        if(type(age) == str): person_dataNew["age"] = age

        loop.run_until_complete(do_update(person_data, person_dataNew))
        return PersonUpdate(person=person_dataNew)
        
class ItemDelete(Mutation):
    status = String()

    class Arguments:
        id = String()

    def mutate(parent, info, id):
        data = loop.run_until_complete(do_find_id(id))
        loop.run_until_complete(do_delete_many(data))
        return ItemDelete(status = "ok")
    
class Group(ObjectType):
    id= ID()
    name = String()
    groupType = Field(lambda:GroupType) #id odpovídající groupType
    members = List(Person)

    def resolve_groupType(parent, info):
        try:
            return loop.run_until_complete(do_find_id(parent["groupType"]))
        except:
            return loop.run_until_complete(do_find_id(parent.groupType))

    def resolve_members(parent, info):
        try:
            list=[]
            for personID in parent.members:
                list.append(loop.run_until_complete(do_find_id(personID)))
            return list
        except:
            list=[]
            for personID in parent["members"]:
                list.append(loop.run_until_complete(do_find_id(personID)))
            return list

class GroupCreate(Mutation):
    group = Field(Group)

    class Arguments:
        name = String()
        groupTypeID = String()

    def mutate(parent, info, name, groupTypeID):
        group_data={
            'id':get_id(),
            'name':name,
            'groupType':groupTypeID,
            'members':[]
        }
        loop.run_until_complete(do_insert(group_data))
        print("Created")
        group = Group(
            id=group_data["id"],
            name=group_data["name"],
            groupType=group_data["groupType"],
            members=group_data["members"]
        )
        return GroupCreate(group=group)

class GroupUpdate(Mutation):
    group = Field(Group)

    class Arguments:
        id = ID(required = True)
        name = String()
        groupTypeID = String()

    def mutate(root, info, id, name=None, groupTypeID=None):
        group_data = loop.run_until_complete(do_find_id(id))
        group_dataNew=copy.deepcopy(group_data)
        if(type(name) == str): group_dataNew["name"] = name
        if(type(groupTypeID) == str): group_dataNew["groupType"] = groupTypeID

        loop.run_until_complete(do_update(group_data, group_dataNew))

        return GroupUpdate(group = group_dataNew)

class AddPersonToGroup(Mutation):
    class Arguments:
        personID=String(required=True)
        groupID=String(required=True)
        roleTypeID=String(required=True)

    group=Field(Group) 
    person=Field(Person) 

    def mutate(root, info, personID, groupID, roleTypeID):
        Group = loop.run_until_complete(do_find_id(groupID)) 
        Person = loop.run_until_complete(do_find_id(personID)) 
        
        GroupNew=copy.deepcopy(Group)
        GroupNew["members"].append(personID)
        loop.run_until_complete(do_update(Group, GroupNew))

        PersonNew=copy.deepcopy(Person)
        PersonNew["memberships"].append([groupID,roleTypeID])
        loop.run_until_complete(do_update(Person, PersonNew))

        return AddPersonToGroup(group=GroupNew,person=PersonNew)

class RemovePersonFromGroup(Mutation):
    class Arguments:
        personID=String(required=True)
        groupID=String(required=True)

    group=Field(Group) 
    person=Field(Person) 

    def mutate(root, info, personID, groupID):
        Group = loop.run_until_complete(do_find_id(groupID)) 
        Person = loop.run_until_complete(do_find_id(personID)) 
        
        GroupNew=copy.deepcopy(Group)
        if personID in loop.run_until_complete(do_find_id(groupID))["members"]: GroupNew["members"].remove(personID)
        loop.run_until_complete(do_update(Group, GroupNew))

        PersonNew=copy.deepcopy(Person)
        for membership in PersonNew["memberships"]: 
            if membership[0]==groupID:
                PersonNew["memberships"].remove(membership)
        loop.run_until_complete(do_update(Person, PersonNew))

        return RemovePersonFromGroup(group=GroupNew, person=PersonNew)

class RoleType(ObjectType):
    id= String()
    name = String()

class RoleTypeCreate(Mutation):
    class Arguments:
        name = String()

    roleType = Field(RoleType)

    def mutate(root, info, name=None):
        roletype_data={
            'id':get_id(),
            'name':name
        }
        loop.run_until_complete(do_insert(roletype_data))
        roletype=RoleType(
            id=roletype_data['id'],
            name=roletype_data['name']
        )
        return RoleTypeCreate(roleType=roletype)

class RoleTypeUpdate(Mutation):
    class Arguments:
        id = String(required=True)
        name = String()

    roleType = Field(RoleType)

    def mutate(parent, info, id, name=None):
        roletype_data = loop.run_until_complete(do_find_id(id))
        roletype_dataNew=copy.deepcopy(roletype_data)
        if(type(name) == str): roletype_dataNew["name"] = name

        loop.run_until_complete(do_update(roletype_data, roletype_dataNew))
        return RoleTypeUpdate(roleType=roletype_dataNew)

class GroupType(ObjectType):
    id= String()
    name = String()

class GroupTypeCreate(Mutation):
    class Arguments:
        name = String()

    groupType = Field(RoleType)

    def mutate(root, info, name=None):
        grouptype_data={
            'id':get_id(),
            'name':name
        }
        loop.run_until_complete(do_insert(grouptype_data))
        grouptype=RoleType(
            id=grouptype_data['id'],
            name=grouptype_data['name']
        )
        return GroupTypeCreate(groupType=grouptype)

class GroupTypeUpdate(Mutation):
    class Arguments:
        id = String(required=True)
        name = String()

    groupType = Field(RoleType)

    def mutate(parent, info, id, name=None):
        grouptype_data = loop.run_until_complete(do_find_id(id))
        grouptype_dataNew=copy.deepcopy(grouptype_data)
        if(type(name) == str): grouptype_dataNew["name"] = name

        loop.run_until_complete(do_update(grouptype_data, grouptype_dataNew))
        return GroupTypeUpdate(groupType=grouptype_dataNew)

class Membership(ObjectType):
    roleType = Field(RoleType)
    group = Field(Group)
