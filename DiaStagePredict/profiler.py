def generateProfile(data):
    Person_Profile = []
    for x in data:
        newStrings = x.replace('_'," ") + '  :  ' + data[x]
        Person_Profile.append(newStrings)
    print(Person_Profile)
    return Person_Profile

def generateOutput(prediction):
    base = 'From the given profile our model has predicted : '
    choice = ['The person does not suffer from diabetes.','The person does suffer from diabetes.']
    
    return base + choice[prediction]