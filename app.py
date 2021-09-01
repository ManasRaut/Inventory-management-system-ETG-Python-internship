from inventory import Inventory as inventory
from cli import CLI as cli

dashboard = '''
---------------------------------------------------
Inventory Management System

1. 1. Place order
2. stock up inventory
3. History
4. view inventory copy

---------------------------------------------------
'''

cmd = -1
# main while loop
while cmd != 5:
    print(dashboard)
    cmd = int(input('> '))

    if cmd == 1:
        pass
    elif cmd == 2:
        pass
    elif cmd == 3:
        pass
    elif cmd == 4:
        pass
    else:
        pass

print('\nExiting... ')