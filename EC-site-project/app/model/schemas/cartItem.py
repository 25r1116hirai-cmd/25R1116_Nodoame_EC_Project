class CartItem:
    def __init__(self, item_id, item_name, price, image_name, amount=1):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.image_name = image_name
        self.amount = amount

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)