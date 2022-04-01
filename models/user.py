class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.promotion_limits = []


class PromotionLimit:
    def __init__(self, promotion_id, amount):
        self.promotion_id = promotion_id
        self.amount = amount
