### Overview
这是一个提供授权服务的后端应用程序。
程序使用 
- Flask 框架搭建
- Docker 独立运行程序
- pytest 构建测试用例

使用到的 python 第三方库：
- [secrets](https://pypi.org/project/python-secrets/)：使用 `token_hex` 用于生成高度加密的随机数作为 Token。
- [passlib](https://pypi.org/project/passlib/)：使用 `sha256_crypt` 对密码进行 sha256 加密（生成一个 hash 值）。在验证的时候通过对输入的密码计算 hash 值，比较新旧的 hash 值进行验证。

### Requirements
- 需要安装 Docker。
- 应用运行在本地的 `5050` 端口，请确保该端口未被占用。



### How to Run 
该应用使用 Docker 和 Flask 进行搭建。
首先，把工程下载到本地 （`git clone`）。
然后，在工程根目录下编译 Docker 文件：
```
docker-compose up --build
```
当编译结束，当能看到一下提示信息时，说明应用已经启动：
```
auth_1  |  * Serving Flask app 'app'
auth_1  |  * Running on all addresses (0.0.0.0)
auth_1  |  * Running on http://127.0.0.1:5050
```

到这里，程序已经成功在本地运行了，可以通过 `Insomnia` 对 API 进行访问，例如 `Create User` 可以使用一下 Curl，更多信息可以查阅下面的 `API Design`。
```
curl --request POST \
  --url http://127.0.0.1:5050/auth/user \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "Lohins",
	"password": "Hello World"
}'
```

在程序已经在 Docker 中运行的前提下，可使用以下命令执行测试：
```
docker exec -it hsbc-auth_auth_1 pytest
```


### APIs Design
**注意**：由于没有使用数据可持久化工具，数据都是存储在内存中的，在项目中对应 `DataStorage` 这个类。 
##### Create User
描述：通过提供的用户名和密码创建一个新用户。密码通过 sha256 加密的方式存储。如果用户名已存在，则返回错误信息。

方法： `post`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| user_name | String | 用户名 |
| password | String | 密码 |

返回值：
1. Status Code `201(Created)`: 成功创建
2. Status Code `400(Bad Request)`: 用户名已存在，返回错误信息 `User does exist!`。

Curl：
```
curl --request POST \
  --url http://127.0.0.1:5050/auth/user \
  --header 'Content-Type: application/json' \
  --data '{
	"user_name": "Lohins",
	"password": "Hello World"
}'
```


##### Delete User
描述：根据提供的用户名，如果找到对应的用户，则删除该用户。如果未找到对应用户，则返回错误信息 。

方法： `delete`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| user_name | String | 想要删除的用户名 |

返回值：
1. Status Code `204 (No Content)`: 成功删除用户。
2. Status Code `400 (Bad Request)`: 用户名不存在，返回错误信息 `User does not exist!`。

Curl:
```
curl --request DELETE \
  --url http://127.0.0.1:5050/auth/user \
  --header 'Content-Type: application/json' \
  --data '{
	"user_name": "Lohins"
}'
```


##### Create Role
描述：通过提供的角色名称，如果角色不存在的话，创建一个新角色。如果角色已经存在，则返回错误信息。

方法： `post`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| role_name | String | 角色名称 |


返回值：
1. Status Code `201(Created)`: 成功创建
2. Status Code `400(Bad Request)`: 角色名称已存在，返回错误信息 `Role does exist!`

Curl：
```
curl --request POST \
  --url http://127.0.0.1:5050/auth/role \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "Admin"
}'
```

##### Delete Role
描述：根据提供的 Role 名称，如果找到对应的 Role，则删除该 Role，并且删除和用户相关的记录。如果未找到对应 Role，则返回错误信息 。

方法： `delete`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| role_name | String | 角色名称 |

返回值：
1. Status Code `204 (No Content)`: 成功删除 Role。
2. Status Code `400 (Bad Request)`: 如果 Role 不存在，返回错误信息 `Role does not exist!`。

Curl:
```
curl --request DELETE \
  --url http://127.0.0.1:5050/auth/role \
  --header 'Content-Type: application/json' \
  --data '{
	"role_name": "Admin"
}'
```


##### Add Role to User
描述：根据提供的 User Name 和 Role Name，如果用户没有被添加到该 Role，则添加该 Role。如果用户已经具有该 Role，则什么都不做 。对于 User Name 和 Role Name 不存在的情况，返回对应错误信息。

方法： `post`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| user_name | String | 用户名 |
| role_name | String | 角色名称 |

返回值：
1. Status Code `200 (OK)`: 成功为用户添加 Role，或者用户已经具有 Role，则什么都不做。
2. Status Code `400 (Bad Request)`: 如果 User Name 和 Role Name 不存在的情况，返回对应错误信息 `User does not exist!` 或者 `Role does not exist!`。

Curl:
```
curl --request POST \
  --url http://127.0.0.1:5050/auth/user/role \
  --header 'Content-Type: application/json' \
  --data '{
	"user_name": "Lohins",
	"role_name": "Admin"
}'
```

##### Authenticate
描述：根据提供的 User Name 和 Password，进行 sha256 hash 验证。如果验证通过，则创建一个新的随机数作为 Token，并返回。如果验证没有通过，则返回错误信息。

方法： `post`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| user_name | String | 用户名 |
| password | String | 密码 |

返回值：
1. Status Code `201 (Created)`: 验证通过并创建新的 Token。
2. Status Code `400 (Bad Request)`: 用户名和密码没有通过验证，或者用户名不存在都会返回 `The user name and password do not match.`。

Curl:
```
curl --request POST \
  --url http://127.0.0.1:5050/auth/token \
  --header 'Content-Type: application/json' \
  --data '{
	"user_name": "Lohins",
	"password": "Hello World"
}'
```

Response sample:
```
{
	"expired_at": 1664206895.336651,
	"token": "2323215f7249acd41979dbe4b76ffb4709aef49cbb87e3875965d16181f6"
}
```

##### Invalidate Token
描述：根据提供的 token，使其失效。使 Token 失效的具体做法是把这个 Token 的过期时间改成过去的一个时间点。

方法： `delete`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| token | String | 令牌 |


返回值：
1. Status Code `200 (Ok)`: 成功使 Token 失效。
2. Status Code `400 (Bad Request)`: 如果 token 已经失效了，返回信息 `Token has been expired.`，如果 token 不存在，返回信息 `Token does not exist.` 。

Curl:
```
curl --request DELETE \
  --url http://127.0.0.1:5050/auth/token \
  --header 'Content-Type: application/json' \
  --data '{
	"token": "XXXX"
}'
```


##### Check Role
描述：根据提供的 token 和 Role，验证 token 对应的用户是否具有该 Role，如果有返回 True，如果没有返回 False。

方法： `get`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| token | String | 令牌 |
| role | String | 角色名称 |


返回值：
1. Status Code `200 (Ok)`: 返回 `{ result: True }` 如果用户具有该 role，返回 `{ result: False }` 如果用户不具有该 role。
2. Status Code `400 (Bad Request)`: 如果 token 已经失效了，返回信息 `Token has been expired.`，如果 token 不存在，返回信息 `Token does not exist.` 。

Curl:
```
curl --request GET \
  --url http://127.0.0.1:5050/auth/role_check \
  --header 'Content-Type: application/json' \
  --data '{
	"token": "XXXX",
	"role": "Admin"
}'
```

Response sample：
```
{
	"result": false
}
```


##### Get All Roles
描述：根据提供的 token，获取该用户所具有的的所有 Role。如果 Token 不是合法的，则返回对应错误信息。

方法： `get`

JSON 参数：

| 名称 | 类型 | 描述 |  
| ----------- | ----------- | ----------- |  
| token | String | 令牌 |

返回值：
1. Status Code `200 (Ok)`: 返回 `{ 'roles': all_roles }`。
2. Status Code `400 (Bad Request)`: 如果 token 已经失效了，返回信息 `Token has been expired.`，如果 token 不存在，返回信息 `Token does not exist.` 。

Curl:
```
curl --request GET \
  --url http://127.0.0.1:5050/auth/roles \
  --header 'Content-Type: application/json' \
  --data '{
	"token": "2323215f7249acd41979dbe4b76ffb4709aef49cbb87e3875965d16181f6"
}'
```

Response sample：
```
{
	"roles": [
		"Member",
		"Admin"
	]
}
```
