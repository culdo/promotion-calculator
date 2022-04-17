class Order:
    def __init__(self, order_id, user, items, promotion):
        self.order_id = order_id
        self.user = user
        self.items = items
        self.promotion = promotion
        if promotion.limit is not None:
            self.promotion.limit.check(self)

        self._calc_item_total()
        self._calc_adjustment_total()
        self.payment_total = self.item_total - self.discount_total

    def _calc_item_total(self):
        self.item_total = 0
        for p in self.items:
            self.item_total += p.price

    def _calc_adjustment_total(self):
        self.discount_total = 0
        if self.promotion.rule.is_eligible(self) and (
                self.promotion.limit is None or self.promotion.limit.is_eligible(self)):
            self.computed_discount = self.promotion.action.perform(self)
            if self.promotion.limit is not None:
                self.promotion.limit.perform(self)
