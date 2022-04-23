from graphene import ObjectType, InputObjectType, Mutation, String, Int, Field
from database import do_insert, do_update, do_delete_many
import asyncio

loop = asyncio.get_event_loop()

''' All that user can contain, graphql display '''
class User(ObjectType):
    name = String()
    group = String()
    phone = Int()
    age = Int()
    incomeY = Int()
    actualDebt = Int()
    city = String()
    street = String()
    primarySchool = String()
    secondarySchool = String()

''' All that can be input to user '''
class UserInput(InputObjectType):
    #name = String(required=True)
    name = String()
    group = String()
    phone = Int()
    age = Int()
    incomeY = Int()
    actualDebt = Int()
    city = String()
    street = String()
    primarySchool = String()
    secondarySchool = String()

''' ***** Start of CUD of CRUD section ***** '''

''' Not sure what exactly they do, should be studied and simplified !!! '''
class UserCreate(Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = Field(User)

    def mutate(root, info, user_data=None):
        loop.run_until_complete(do_insert(user_data))
        print("Created")
        user = User(
            name=user_data.name,
            group=user_data.group
        )
        return UserCreate(user=user)

class UserUpdate(Mutation):
    class Arguments:
        user_data = UserInput(required=True)
        new_data = UserInput(required=True)

    user = Field(User)

    def mutate(root, info, user_data=None, new_data=None):
        loop.run_until_complete(do_update(user_data, new_data))
        print("Updated")
        user = User(
            name=new_data.name,
            group=new_data.group
        )
        return UserUpdate(user=user)

class UserDelete(Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = Field(User)

    def mutate(root, info, user_data=None):
        loop.run_until_complete(do_delete_many(user_data))
        print("Deleted")
        user = User(
            name=user_data.name,
            group=user_data.group
        )
        return UserDelete(user=user)

''' ***** End of CUD of CRUD section ***** '''