class SessionManager:
    _current_user_id = None

    @classmethod
    def set_current_user_id(cls, user_id):
        cls._current_user_id = user_id

    @classmethod
    def get_current_user_id(cls):
        return cls._current_user_id
