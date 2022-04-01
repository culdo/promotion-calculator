from ..order import date
import calendar


class Promotion:
    def __init__(self, pid, rule, action,
                 usage_limits=None, amount_per_user_limits=None, amount_per_month_limits=None):
        self.pid = pid
        if amount_per_month_limits is not None:
            self.update_time()
        self.rule = rule
        self.action = action
        self.usage_limits = usage_limits
        self.amount_per_user_limits = amount_per_user_limits
        self.amount_per_month_limits = amount_per_month_limits
        self.amount_per_month_limits_save = amount_per_month_limits

    def update_time(self):
        self.start_time = date.today().replace(day=1)
        last_day = calendar.monthrange(date.today().year, date.today().month)[-1]
        self.end_time = date.today().replace(day=last_day)
