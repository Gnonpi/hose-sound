class HoseError(Exception):
    """
    Base exception for Hose
    """


class UserNotBelongingToHose(HoseError):
    def __init__(self, user_passed, hose):
        self.id_user_passed = user_passed.id_user
        self.id_hose = hose.id_hose
        self.expected_id_user_a = hose.id_user_a
        self.expected_id_user_b = hose.id_user_b

    def __str__(self):
        return f"User({self.user_passed.id_user}) attempted to access " \
               f"Hose({self.id_hose})[{self.expected_id_user_a}-{self.expected_id_user_b}]"
