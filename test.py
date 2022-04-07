from datetime import date
from unittest.mock import patch

from models.order import Order
from models.product import Product
from models.promotion import Promotion
from models.promotion.action import FlatPercentDiscount, FlatRateDiscount, CreatingLineItems
from models.promotion.limit import UsageLimit, PerUserLimit, PerMonthLimit
from models.promotion.rule import ItemTotalRule, ProductRule
from models.user import User
import unittest


class TestOrder(unittest.TestCase):
    # 訂單滿 X 元折 Z %
    def test_order1(self, x=100, z=15):
        user = User(user_id=1)
        promotion = Promotion(pid=1, rule=ItemTotalRule(amount_min=x),
                              action=FlatPercentDiscount(flat_percent=z))
        items = [Product(product_id=1, price=20),
                 Product(product_id=2, price=30),
                 Product(product_id=3, price=40)]
        order = Order(order_id=11, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 90, "wrong item_total")
        self.assertEqual(order.discount_total, 0, "wrong discount_total")
        self.assertEqual(order.payment_total, 90, "wrong payment_total")
        items = [Product(product_id=4, price=30),
                 Product(product_id=5, price=40),
                 Product(product_id=6, price=50)]
        order = Order(order_id=12, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 18, "wrong discount_total")
        self.assertEqual(order.payment_total, 102, "wrong payment_total")

    # 特定商品滿 X 件折 Y 元
    def test_order2(self, product_id=2, x=2, y=30):
        user = User(user_id=2)
        promotion = Promotion(pid=2, rule=ProductRule(product_id=product_id, qty=x),
                              action=FlatRateDiscount(amount=y))
        items = [Product(product_id=1, price=20),
                 Product(product_id=2, price=30),
                 Product(product_id=3, price=40)]
        order = Order(order_id=21, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 90, "wrong item_total")
        self.assertEqual(order.discount_total, 0, "wrong discount_total")
        self.assertEqual(order.payment_total, 90, "wrong payment_total")
        items = [Product(product_id=2, price=30),
                 Product(product_id=2, price=30),
                 Product(product_id=6, price=50)]
        order = Order(order_id=22, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 110, "wrong item_total")
        self.assertEqual(order.discount_total, 30, "wrong discount_total")
        self.assertEqual(order.payment_total, 80, "wrong payment_total")

    # 訂單滿 X 元贈送特定商品
    def test_order3(self, x=100, pid=2):
        user = User(user_id=3)
        items = [Product(product_id=1, price=30),
                 Product(product_id=2, price=40),
                 Product(product_id=3, price=50)]
        promotion = Promotion(pid=3, rule=ItemTotalRule(amount_min=x),
                              action=CreatingLineItems(pid))
        order = Order(order_id=3, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 0, "wrong discount_total")
        self.assertEqual(order.payment_total, 120, "wrong payment_total")
        target_items = [Product(product_id=1, price=30),
                        Product(product_id=2, price=40),
                        Product(product_id=3, price=50),
                        Product(product_id=2)]
        for order_i, target_i in zip(order.items, target_items):
            self.assertTrue(order_i.product_id == target_i.product_id and order_i.price == target_i.price, "items wrong")

    # 訂單滿 X 元折 Y 元,此折扣在全站總共只能套用 N 次
    def test_order4(self, x=100, y=30, n=2):
        user = User(user_id=4)
        items = [Product(product_id=1, price=30),
                 Product(product_id=2, price=40),
                 Product(product_id=3, price=50)]
        promotion = Promotion(pid=4, rule=ItemTotalRule(amount_min=x),
                              action=FlatRateDiscount(amount=y), limit=UsageLimit(n))
        order = Order(order_id=41, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 30, "wrong discount_total")
        self.assertEqual(order.payment_total, 90, "wrong payment_total")
        order = Order(order_id=42, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 30, "wrong discount_total")
        self.assertEqual(order.payment_total, 90, "wrong payment_total")
        order = Order(order_id=43, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 0, "wrong discount_total")
        self.assertEqual(order.payment_total, 120, "wrong payment_total")

    # 訂單滿 X 元折 Z %,折扣每人只能總共優惠 N 元
    def test_order5(self, x=100, z=30, n=50):
        items = [Product(product_id=1, price=30),
                 Product(product_id=2, price=40),
                 Product(product_id=3, price=50)]
        promotion = Promotion(pid=5, rule=ItemTotalRule(amount_min=x),
                              action=FlatPercentDiscount(flat_percent=z), limit=PerUserLimit(n))
        user = User(user_id=51)
        order = Order(order_id=51, user=user, items=items, promotion=promotion)
        self.assertEqual(user.user_id, 51, "wrong user_id")
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 36, "wrong discount_total")
        self.assertEqual(order.payment_total, 84, "wrong payment_total")
        user = User(user_id=52)
        order = Order(order_id=52, user=user, items=items, promotion=promotion)
        self.assertEqual(user.user_id, 52, "wrong user_id")
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 36, "wrong discount_total")
        self.assertEqual(order.payment_total, 84, "wrong payment_total")
        order = Order(order_id=53, user=user, items=items, promotion=promotion)
        self.assertEqual(user.user_id, 52, "wrong user_id")
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 14, "wrong discount_total")
        self.assertEqual(order.payment_total, 106, "wrong payment_total")

    # 訂單滿 X 元折 Y 元,此折扣在全站每個月折扣上限為 N 元
    def test_order6(self, x=100, y=30, n=50):
        user = User(user_id=5)
        items = [Product(product_id=1, price=30),
                 Product(product_id=2, price=40),
                 Product(product_id=3, price=50)]
        promotion = Promotion(pid=6, rule=ItemTotalRule(amount_min=x),
                              action=FlatRateDiscount(amount=y), limit=PerMonthLimit(n))
        order = Order(order_id=61, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 30, "wrong discount_total")
        self.assertEqual(order.payment_total, 90, "wrong payment_total")
        order = Order(order_id=62, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 20, "wrong discount_total")
        self.assertEqual(order.payment_total, 100, "wrong payment_total")
        order = Order(order_id=63, user=user, items=items, promotion=promotion)
        self.assertEqual(order.item_total, 120, "wrong item_total")
        self.assertEqual(order.discount_total, 0, "wrong discount_total")
        self.assertEqual(order.payment_total, 120, "wrong payment_total")

        next_month = date.today().replace(month=(date.today().month + 1) % 12)

        with patch('models.promotion.limit.date') as mock_date:
            mock_date.today.return_value = next_month
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            order = Order(order_id=64, user=user, items=items, promotion=promotion)
            self.assertEqual(order.item_total, 120, "wrong item_total")
            self.assertEqual(order.discount_total, 30, "wrong discount_total")
            self.assertEqual(order.payment_total, 90, "wrong payment_total")


if __name__ == '__main__':
    unittest.main()
