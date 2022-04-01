from datetime import date
from models.user import PromotionLimit


class Order:
    def __init__(self, order_id, user, items, promotion):
        self.order_id = order_id
        self.user = user
        self.items = items
        self.promotion = promotion
        self._check_per_user_promotion()
        self._check_per_month_promotion()

        self._calc_item_total()
        self._calc_adjustment_total()
        self.payment_total = self.item_total - self.discount_total

    def _calc_item_total(self):
        self.item_total = 0
        for p in self.items:
            self.item_total += p.price

    def _calc_adjustment_total(self):
        self.discount_total = 0
        if self.promotion.rule.is_eligible(self):
            discount = self.promotion.action.perform(self)
            self._calc_usage_limits()
            self._calc_amount_per_month_limits(discount)
            self._calc_amount_per_user_limits(discount)

    def _calc_usage_limits(self):
        if self.promotion.usage_limits is not None:
            if self.promotion.usage_limits > 0:
                self.promotion.usage_limits -= 1
            else:
                self.discount_total = 0

    def _check_per_month_promotion(self):
        if self.promotion.amount_per_month_limits is not None \
                and date.today() > self.promotion.end_time:
            self.promotion.amount_per_month_limits = self.promotion.amount_per_month_limits_save
            self.promotion.update_time()

    def _calc_amount_per_month_limits(self, discount):
        if self.promotion.amount_per_month_limits is not None:
            if self.promotion.amount_per_month_limits <= 0:
                self.discount_total = 0
                return
            if self.promotion.amount_per_month_limits - self.discount_total > 0:
                self.promotion.amount_per_month_limits -= self.discount_total
            elif self.promotion.amount_per_month_limits - self.discount_total <= 0:
                # fallback and discount rest limits
                self.discount_total = self.discount_total - discount + self.promotion.amount_per_month_limits
                self.promotion.amount_per_month_limits = 0

    def _check_per_user_promotion(self):
        if self.promotion.amount_per_user_limits is not None:
            new_user_promotion = True
            for pl in self.user.promotion_limits:
                if pl.promotion_id == self.promotion.pid:
                    new_user_promotion = False
            if new_user_promotion:
                self.user.promotion_limits.append(PromotionLimit(self.promotion.pid,
                                                                 self.promotion.amount_per_user_limits))

    def _calc_amount_per_user_limits(self, discount):
        if len(self.user.promotion_limits) > 0:
            for pl in self.user.promotion_limits:
                if pl.promotion_id == self.promotion.pid:
                    if pl.amount <= 0:
                        self.discount_total = 0
                        return
                    if pl.amount - self.discount_total > 0:
                        pl.amount -= self.discount_total
                    elif pl.amount - self.discount_total <= 0:
                        # fallback and discount rest limits
                        self.discount_total = self.discount_total - discount + pl.amount
                        pl.amount = 0
