class CartD:
    def __init__(
        self,
        lineNo, 
        itemId, 
        amount,
        price,
        tax,
        ):
        
        self.lineNo = lineNo
        self.itemId = itemId
        self.amount = amount
        self.price = price
        self.tax = tax
                

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)