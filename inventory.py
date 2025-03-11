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
            if self.items[item.name]['quantity'] > quantity:
                self.items[item.name]['quantity'] -= quantity
            else:
                del self.items[item.name]

        else:
            print(f"You don't have {item.name} in your inventory.")

    def display_inv(self):
        print("Inventory")
        for item_name, item_data in self.items.items():
            print(f"- {item_name}: {item_data["quantity"]}")

