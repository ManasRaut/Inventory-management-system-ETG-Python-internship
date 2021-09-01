import json

class Inventory():
    def __init__(self):
        self.records = []
    
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
