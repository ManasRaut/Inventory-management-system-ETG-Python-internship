import json
import time
from cli import CLI

class Inventory():
    def __init__(self):
        self.records = []
        self.cli  = CLI()
    
    def log(self, res, order):
        fh = open("history.log", "a")
        logline = "\n" + time.ctime() + "| " + res + str(order)
        fh.write(logline)
        fh.close()
    
    def read_records(self):
        fh = open('records.json', "r")
        self.records = json.loads(fh.read())
        fh.close()
    
    def handle_order(self, id, qty):
        itm = None
        order = None
        for item in self.records:
            if item["id"] == id:
                order = item.copy()
                order["instock"] = order["qty"]
                order["qty"] = qty
                itm = item
                break
        if itm:
            if itm["qty"] == 0:
                return ("OUTOFSTOCK", order)
            elif itm["qty"] < order["qty"]:
                return ("FEWINSTOCK", order)
            else:
                return ("INSTOCK", order)
        else:
            return ("NOITEMPRESENT", order)
    
    def update_records(self):
        fh = open('records.json', "w")
        try:
            fh.write(json.dumps(self.records, indent = 4))
            fh.close()
            self.read_records()
            return True
        except:
            return False

    def deduct_inventory(self, order):
        for item in self.records:
            if item["id"] == order["id"]:
                item["qty"] = item["qty"] - order["qty"]
                return True
        return False

    def get_bill(self, order):
        bill = '''
        ***************************************************
        Bill No.\t{}
        Item Id:\t{}
        Name:\t{}
        Price:\t{}

        Requested Quantity:\t{}
        ---------------------------------------------------
        Total Amount:\tRs. {}
        ***************************************************
        '''.format("temp", order["id"], order["name"], order["price"], order["qty"], order["qty"] * order["price"])

        return bill

    def stockUp(self, id):
        self.read_records()
        itm = None
        for item in self.records:
            if item["id"] == id:
                itm = item
                break
        if itm:
            itm["name"] = (input("Enter Item name: ") or itm["name"])
            itm["price"] = int(input("Enter price: ") or itm["price"])
            itm["qty"] = int(input("Enter current stock: ") or itm["qty"])
            self.update_records()
            self.log("ITEM_STOCKED_UP", itm)
            self.cli.success("\nSuccessfully stocked up")
        else:
            self.cli.failed("\nNo such item exists")
    
    def add_new_item(self, itm):
        self.read_records()
        for item in self.records:
            if item["id"] == itm["id"]:
                return False
        self.records.append(itm)
        self.update_records()
        return True