class CartItem:
    def __init__(
        self, 
        orderId, 
        orderDate, 
        userName,
        orderAddress,
        cardNum,
        shipFlg,
        price, 
        tax,
        shipping,
        total,
        detail
        ):
        
        self.orderId = orderId
        self.orderDate = orderDate
        self.userName = userName
        self.orderAddress = orderAddress
        self.cardNum = cardNum
        self.shipFlg = shipFlg
        self.price = price
        self.tax = tax
        self.shipping = shipping
        self.total = total
        self.detail = detail
        

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)