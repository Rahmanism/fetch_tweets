
#%%
from random import sample

names = 'mammad amir ali hosein mahdi mostafa ahmad mohsen'.split()
sample(names, 2)


#%%
f = 123_456_789
print(f)
print(format(f,','))
print(f)


#%%
n = 'mammad ali asqar'.split()
a = '10 15 18'.split()
dict(zip(n,a))


#%%
colors = 'red green blue yellow brown white black'.split()
import random

color = random.choice(colors)
print(color)
# is it primary color?
color in 'red yellow blue'.split()


#%%
def apply_discount(product, discount):
    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price']
    return price


#%%
shoes = {'name': 'Fancy Shoes', 'price': 14900}
print(apply_discount(shoes, .2))
print(apply_discount(shoes, 2))


#%%
def foo(value):
    if value:
        return value


#%%
print(foo(5))
print(foo(None))
print(type(foo(0)))


#%%
a = ['Ali', 'Behnam', 'Hosein' 'Majid']
a


#%%
string1 = ('This is kind of multi '
          'line text using the above '
          'method!')
print(string1)


#%%
class TestUnderScore:
    def __init__(self):
        self.foo = 11
        self._bar = 23

t = TestUnderScore()
print(t.foo)
print(t._bar)


#%%
class Test:
    def __init__(self):
        self.foo = 11
        self._bar = 12
        self.__baz = 12


#%%
t = Test()
dir(t)
print(t._Test__baz)
t._Test__baz = 14
print(t._Test__baz)


#%%
class ExtendedTest(Test):
    def __init__(self):
        super().__init__()
        self.foo = 'overridden'
        self._bar = 'overridden'
        self.__baz = 'overridden'


#%%
t2 = ExtendedTest()
t2.foo
t2._ExtendedTest__baz
t2._Test__baz


#%%
dir(t2)


