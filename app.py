from inventory import Inventory
from cli import CLI
import os
from pathlib import Path
import time

dashboard = '''
---------------------------------------------------
Inventory Management System

1. Place order
2. stock up inventory
3. History
4. view inventory copy

---------------------------------------------------
'''

def printError():
    print("\n*******ERROR******\n")

inventory = Inventory()
cli = CLI()
cmd = -1
# main while loop
while cmd != 5:
    print(dashboard)
    cmd = int(input('> ') or -1)

    if cmd == 1:
        inventory.read_records()
        id = input("Enter id: ")
        qty = int(input("Enter quantity: "))
        result, order = inventory.handle_order(id, qty)

        if result == "OUTOFSTOCK": # done
            print("Oops, sorry out of stock!!!")
            continue
        elif result == "FEWINSTOCK": # done
            print('''
            Requested items: {}
            Items in stock: {}
            '''.format(order["qty"], order["instock"]))
            ans = input("Do you want to buy remaining {} items ? (Y or N): ".format(order["instock"]))
            if ans == "N":
                print("OK order cancelled")
                inventory.log("ORDER_CANCELED", order)
                continue
            elif ans == "Y":
                order["qty"] = order["instock"]
        elif result == "NOITEMPRESENT": # incomplete
            print("No Item Exists")
            continue

        res = inventory.deduct_inventory(order)
        res &= inventory.update_records()
        inventory.log("ITEM_DEDUCTED", order)
        if res:
            print(inventory.get_bill(order))
        else:
            printError()
            
    elif cmd == 2:
        c = int(input("\n1. STock up existing item.\n2. Add new Item.\n\n> "))
        if c == 1:
            id = input("Enter id: ")
            inventory.stockUp(id)
        elif c == 2:
            itm = {}
            itm["id"] = input("Enter id: ")
            itm["name"] = input("Enter Item name: ")
            itm["price"] = int(input("Enter price: ") or 100)
            itm["qty"] = int(input("Enter current stock: ") or "0")
            if itm["id"] and itm["name"]:
                inventory.add_new_item(itm)
            else:
                print("Please enter valid details")
    elif cmd == 3:
        os.startfile("history.log")
    elif cmd == 4:
        home = Path.home()
        name = (time.ctime() + ".json").replace(":", "-")
        path = os.path.join(home, "Documents", "InventorySystem")
        if not os.path.exists(path):
            os.makedirs(path)
        fh = open(path+"\\"+name, "w")
        fh.write(open("records.json", "r").read())
        fh.close()
        os.startfile(path+"\\"+name)
        print("Saved inventory copy", path+"\\"+name)
        inventory.log("INVENTORY_COPY_CREATED", {})
    else:
        pass

print('\nExiting... ')