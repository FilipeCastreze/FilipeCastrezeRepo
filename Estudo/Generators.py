from operator import itemgetter


def gen123():
    yield 1
    yield 2
    yield 3

g = gen123()
print(g)

try:
    print(next(g))
    print(next(g))
    print(next(g))
    #print(next(g))
except StopIteration:
    raise ValueError("Iterable is empty")

print("\n")
def take(count,iterable):
    counter = 0
    for item in iterable:
        if counter == count:
            return
        counter += 1
        yield item


def distinct(iterable):
    seen = set()
    for item in iterable:
        if item in seen:
            continue
        yield item
        seen.add(item)


def run_pipeline():
    items = [3, 6, 6, 2, 1, 1]
    for item in take(5, distinct(items)):
        print(item)


run_pipeline()

print("\n")

