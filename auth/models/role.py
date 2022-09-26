from auth.models.utils import DataStorage


class RoleNotFoundError(Exception):
    pass

class RoleDuplicatedError(Exception):
    pass
class Role:

    # 管理全部已经创建的 role。
    created_roles = []

    def __init__(self, name) -> None:
        self.name = name
    

    @classmethod
    def create_role(cls, new_role):
        if next((r for r in DataStorage.roles_table if r.name == new_role), None):
            raise RoleDuplicatedError(f'Role for {new_role} have been existed. Please choose a different name')

        DataStorage.roles_table.append(Role(new_role))
    
    @classmethod
    def delete_role(cls, target):
        filtered_roles = list(filter(lambda r:r.name != target, DataStorage.roles_table))
        
        if len(filtered_roles) == len(DataStorage.roles_table):
            raise RoleNotFoundError(f'Role {target} does not exist. Please try again')

        DataStorage.roles_table = filtered_roles

        # remove user roles as well.
        DataStorage.user_role_table = list(filter(lambda r:r.role_name != target, DataStorage.user_role_table))
    
    @classmethod
    def get_role(cls, name):
        filtered_roles = list(filter(lambda r:r.name == name, DataStorage.roles_table))

        if not filtered_roles:
            return None
        
        return filtered_roles[0]
