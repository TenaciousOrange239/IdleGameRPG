from items import Item

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self,item,quantity=1):
        if item in self.items:
            self.items[item.name]["quantity"] += quantity
        else:
            self.items[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self,item,quantity=1):
        if item in self.items:

