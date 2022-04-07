class Promotion:
    def __init__(self, pid, rule, action, limit=None):
        self.pid = pid
        self.limit = limit
        self.rule = rule
        self.action = action
