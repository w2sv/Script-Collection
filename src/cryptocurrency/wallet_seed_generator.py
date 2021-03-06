import string
import random


LENGTH = 81
POOL = string.ascii_letters + '9'


print(''.join([random.choice(POOL) for _ in range(LENGTH)]).upper())
