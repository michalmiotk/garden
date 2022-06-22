import json


Dictionary ={(1, 2, 3):'Welcome', 2:'to',
			3:'Geeks', 4:'for',
			5:'Geeks'}


# Our dictionary contains tuple
# as key, so it is automatically
# skipped If we have not set
# skipkeys = True then the code
# throws the error
json_string = json.dumps(Dictionary,
						skipkeys = True)

with open("a", 'w') as r:
    r.write(json_string)
