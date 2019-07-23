names = ['Hal', 'Clark', 'Charles'] 
supernames = ['Green Lantern', 'Superman', 'Professor X']
​
hero_dict = {}
for name, super in zip (names, supernames):
    hero_dict[name] = super
print(hero_dict)
​
# {'Hal': 'Green Lantern', 'Clark': 'Superman', 'Charles': 'Professor X'}
​
#Dictionary Comprehension
​
hero_dict = dict(zip(names, supernames))
​
hero_dict2 = {value:key for key,value in hero_dict.items()}
print (hero_dict2)
​
# {'Green Lantern': 'Hal', 'Superman': 'Clark', 'Professor X': 'Charles'}
{'Hal': 'Green Lantern', 'Clark': 'Superman', 'Charles': 'Professor X'}
{'Green Lantern': 'Hal', 'Superman': 'Clark', 'Professor X': 'Charles'}