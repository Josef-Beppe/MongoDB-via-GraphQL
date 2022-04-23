import random
import string

defaultStrs = {'name': 'user_', 'group': 'group_'}
defaultNums = {'phone': (602000000, 777999999)}
extraFields = {'street': '', 'city': '', 'primarySchool': '', 'secondarySchool': ''}
nums = {**defaultNums, 'age': (15, 80), 'incomeY': (300000, 1500000), 'actualDebt': (0, 10000000)}

def randomString(prefix='', N=8):
    return prefix + ''.join(random.choices(string.ascii_uppercase, k=N))

def randomDocument(strs=defaultStrs, nums=defaultNums):
    result = {}
    for key, value in strs.items():
        result[key] = randomString(value)
        #result[key] = value
    for key, value in nums.items():
        result[key] = random.randint(value[0], value[1])
    return result

def heterogenizeDocument(doc, **values):
    result = {**doc}
    for key, value in values.items():
        if random.random() < 0.5:
            result[key] = randomString(key+'_')
    return result

def getFullRndDoc():
    return heterogenizeDocument(randomDocument(defaultStrs, nums), **extraFields)