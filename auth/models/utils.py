class DataStorage:
    users_table = []

    roles_table = []

    user_role_table = []

    user_token_table = []


class EntityNotFoundError(Exception):
    pass

class EntityDuplicatedError(Exception):
    pass
