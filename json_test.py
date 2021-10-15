import json

filename = 'user_settings.json'   

user_settings = [{"user" : "karl",    "asdf" : ["1", "2"]},{"user" : "Rich", "asdf" : ["being sad", "L"]}]
with open(filename, 'w') as file_object:
    json.dump(user_settings, file_object)

with open(filename, 'r') as file_object:
    file = json.load(file_object)
    print(file)
    for files in file:
        user = files["user"]
        asdf = files["asdf"]

   
if user == "karl":
    print("he sucks")

else: 
    print("L")

with open(filename) as fhandle:
    user_settings = json.load(fhandle)



for user_id in user_settings:
    if user_id["user"] == "karl":
        print("asdf")