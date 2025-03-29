class Item:
    def __init__(self,name,quantity,item_type,description,stats=None):
        self.name = name
        self.quantity = quantity
        self.item_type = item_type
        self.description = description
        self.stats = stats
