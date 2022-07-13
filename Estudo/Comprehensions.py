from pprint import pprint as pp
from math import sqrt

"""
List comprehension syntax:
[ expr(item) for item in iterable]
"""
words = "Why sometimes I have believed as many as six impossible things before breakfast".split()
print(words)

print([len(word) for word in words])
print('\n')
"""
Dict comprehensions syntax:
{
    key_expr(item): value_expr(item)
    for item in iterable
}
"""
country_to_capital = {
    'UK': 'London',
    'Brazil': 'Brasilia',
    'Morocco': 'Rabat',
    'Sweden': 'Stockholm'
}
pp(country_to_capital)
print('\n')
capital_to_country = {capital: country for country, capital in country_to_capital.items()}
pp(capital_to_country)

"""
Filtering Comprehensions
"""
def is_prime(x):
    if x<2:
        return False
    for i in range(2, int(sqrt(x))+1):
        if x % i == 0:
            return False
    return True

print([x for x in range(101) if is_prime(x)])

prime_square_divisors = {x*x: (1, x, x*x) for x in range(20) if is_prime(x)}
pp(prime_square_divisors)

"""
Iteration protocol
"""

iterable = ['Spring','Summer','Autumn','Winter']
iterator = iter(iterable)
try:
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
except StopIteration:
    raise ValueError("Iterable is empty")