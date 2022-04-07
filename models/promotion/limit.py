import calendar

from datetime import date
from ..user import PromotionLimit


class Limit:
    def check(self, order):
        pass

    def perform(self, order):
        pass


class UsageLimit(Limit):
    def __init__(self, limits):
        self.usage_limits = limits

    def perform(self, order):
        if self.usage_limits is not None:
            if self.usage_limits > 0:
                self.usage_limits -= 1
            else:
                order.discount_total = 0


class PerMonthLimit(Limit):
    def __init__(self, limits):
        self.amount_per_month_limits = limits
        self.amount_per_month_limits_save = limits
        self._update_time()

    def check(self, order):
        if self.amount_per_month_limits is not None \
                and date.today() > self.end_time:
            self.amount_per_month_limits = self.amount_per_month_limits_save
            self._update_time()

    def perform(self, order):
        if self.amount_per_month_limits is not None:
            if self.amount_per_month_limits <= 0:
                order.discount_total = 0
                return
            if self.amount_per_month_limits - order.discount_total > 0:
                self.amount_per_month_limits -= order.discount_total
            elif self.amount_per_month_limits - order.discount_total <= 0:
                # fallback and discount rest limits
                order.discount_total = order.discount_total - order.computed_discount + self.amount_per_month_limits
                self.amount_per_month_limits = 0

    def _update_time(self):
        self.start_time = date.today().replace(day=1)
        last_day = calendar.monthrange(date.today().year, date.today().month)[-1]
        self.end_time = date.today().replace(day=last_day)


class PerUserLimit(Limit):
    def __init__(self, limits):
        self.amount_per_user_limits = limits

    def check(self, order):
        if self.amount_per_user_limits is not None:
            new_user_promotion = True
            for pl in order.user.promotion_limits:
                if pl.promotion_id == order.promotion.pid:
                    new_user_promotion = False
            if new_user_promotion:
                order.user.promotion_limits.append(PromotionLimit(order.promotion.pid,
                                                                  self.amount_per_user_limits))

    def perform(self, order):
        if len(order.user.promotion_limits) > 0:
            for pl in order.user.promotion_limits:
                if pl.promotion_id == order.promotion.pid:
                    if pl.amount <= 0:
                        order.discount_total = 0
                        return
                    if pl.amount - order.discount_total > 0:
                        pl.amount -= order.discount_total
                    elif pl.amount - order.discount_total <= 0:
                        # fallback and discount rest limits
                        order.discount_total = order.discount_total - order.computed_discount + pl.amount
                        pl.amount = 0
