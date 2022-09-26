from passlib.hash import sha256_crypt

from auth.models.token import Token
from auth.models.user_role import UserRole
from auth.models.utils import DataStorage

class UserNotFoundError(Exception):
    pass

class UserDuplicatedError(Exception):
    pass

class AuthenticateFailError(Exception):
    pass

class User:

    def __init__(self, name, password_hash) -> None:
        self.name = name
        self.password_hash = password_hash
    

    @classmethod
    def create_user(cls, name, password):
        if next((u for u in DataStorage.users_table if u.name == name), None):
            raise UserDuplicatedError(f'The name {name} have been existed. Please choose a different user name')

        password_hash = sha256_crypt.hash(password)
        new_user = User(name,password_hash)

        DataStorage.users_table.append(new_user)

        return new_user

    @classmethod
    def delete_user(cls, name):
        filtered_users = list(filter(lambda u:u.name != name, DataStorage.users_table))
        if len(filtered_users) == len(DataStorage.users_table):
            raise UserNotFoundError(f'The User {name} does not exist. Please try again')
        
        DataStorage.users_table = filtered_users



    @classmethod
    def get_user(cls, name):
        filtered_users = list(filter(lambda u:u.name == name, DataStorage.users_table))

        if not filtered_users:
            return None
        
        return filtered_users[0]

    @classmethod
    def authenticate(self, user_name, password):
        user = User.get_user(user_name)

        if not user:
            raise UserNotFoundError(f'The name {user_name} does not exist. Please try again')            

        token = user.create_token(password)
        return token

    @classmethod
    def check_role(cls, token_str, role):
        target_token = Token.get_token(token_str)
        target_role = next((r for r in DataStorage.user_role_table if r.user_name == target_token.user_name and r.role_name == role), None)

        return target_role is not None
    
    @classmethod
    def get_all_roles(cls, token_str):
        target_token = Token.get_token(token_str)
        matched_roles = filter(lambda r:r.user_name == target_token.user_name, DataStorage.user_role_table)

        return [r.role_name for r in matched_roles]

    def add_role(self, role):
        existing_roles = list(
            filter(
                lambda r:r.user_name == self.name and r.role_name == role.name, 
                DataStorage.user_role_table
            )
        )
        
        # add roles only if the user does not have the role.
        if not existing_roles:
            user_role = UserRole(user_name=self.name, role_name=role.name)
            DataStorage.user_role_table.append(user_role)
    
    def verify(self, password):
        return sha256_crypt.verify(password, self.password_hash)
    
    def create_token(self, password):
        if not self.verify(password):
            raise AuthenticateFailError('The user name and password do not match.')
        
        return Token(self.name)


        
        




