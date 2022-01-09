crucial = ['eggs','ham' ,'cheese']
dishes = {'eggs': 2, 'sausage': 1, 'bacon': 1, 'spam': 500}

for item in crucial:
    if not item in dishes:
        dishes.update({item:{}})

print (dishes)

