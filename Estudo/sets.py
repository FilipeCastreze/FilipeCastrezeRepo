blue_eyes = {'Olivia','Harry','Lily','Jack','Amelia'}
blond_hair = {'Harry','Jack','Amelia','Mia','Joshua'}
smell_hcn = {'Harry','Amelia'}
taste_ptc = {'Harry','Amelia','Lily','Lola'}
o_blood = {'Mia','Joshua','Lily','Olivia'}
b_blood = {'Jack','Amelia'}
a_blood = {'Harry'}
ab_blood = {'Joshua','Lola'}

print('Who has blue eyes OR blond hair?')
print(blue_eyes.union(blond_hair))
print('\nWho has blue eyes AND blond hair?')
print(blue_eyes.intersection(blond_hair))
print("\nWho has blue eyes but doens't have blond hair?")
print(blue_eyes.difference(blond_hair))
print('\nWho has exclusive blue eyes or blond hair, but not both?')
print(blue_eyes.symmetric_difference(blond_hair))

print('\nAre the people who smell hcn blond?')
if (smell_hcn.issubset(blond_hair)):
    print('Yes!')
else:
    print('No!')

print('\nDoes the people that taste ptc smell hcn?')
if (taste_ptc.issuperset(smell_hcn)):
    print('Yes!')
else:
    print('No!')

print('\nIs there anyone with A blood and O blood togheter?')
if (a_blood.isdisjoint(o_blood)):
    print('No!')
else:
    print('Yes!')