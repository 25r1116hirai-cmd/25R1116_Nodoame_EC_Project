class CartItem:
    def __init__(
        self, 
        orderDate, 
        userName,
        orderAddress,
        cardNum,
        price, 
        tax,
        shipping,
        total
        ):
        
        self.orderDate = orderDate
        self.userName = userName
        self.orderAddress = orderAddress
        self.cardNum = cardNum
        self.price = price
        self.tax = tax
        self.shipping = shipping
        self.total = total
        

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)