from models.calculator import FlatPercentItemTotal, FlatRateTotal
from models.product import Product


class Action:
    def __init__(self, calculator):
        self.calculator = calculator

    def perform(self, order):
        discount = self.calculator.compute(order)
        order.discount_total += discount
        return discount


class FlatPercentDiscount(Action):
    def __init__(self, flat_percent):
        super().__init__(FlatPercentItemTotal(flat_percent))

    def perform_line_item(self, order, pid):
        discount = self.calculator.compute_line_item(order, pid)
        order.discount_total += discount


class FlatRateDiscount(Action):
    def __init__(self, amount):
        super().__init__(FlatRateTotal(amount))


class CreatingLineItems(Action):
    def __init__(self, gift_product_id):
        self.gift_product_id = gift_product_id
        super().__init__(None)

    def perform(self, order):
        gift = Product(self.gift_product_id)
        order.items.append(gift)
