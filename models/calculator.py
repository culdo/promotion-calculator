class Calculator:
    def compute(self, order):
        pass


class FlatPercentItemTotal(Calculator):
    def __init__(self, flat_percent):
        self.flat_percent = flat_percent

    def compute(self, order):
        computed_amount = round(order.item_total * self.flat_percent / 100, 2)
        return computed_amount


class FlatRateTotal(Calculator):
    def __init__(self, amount):
        self.amount = amount

    def compute(self, order):
        return self.amount
