class Rule:
    def is_eligible(self, order):
        pass


class ItemTotalRule(Rule):
    def __init__(self, amount_min):
        self.amount_min = amount_min

    def is_eligible(self, order):
        return order.item_total > self.amount_min


class ProductRule(Rule):
    def __init__(self, product_id, qty):
        self.product_id = product_id
        self.qty = qty

    def is_eligible(self, order):
        qty = 0
        for product in order.items:
            if self.product_id == product.product_id:
                qty += 1
        if qty >= self.qty:
            return True
        else:
            return False
