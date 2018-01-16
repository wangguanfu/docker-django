
## IOT 后台接口

## 登录

`server`: **http://127.0.0.1:8000**
`url`: **/users/login**


- 请求方法:**GET**

- 参数:
|note|email|username|password|
|:-:|:-:|:-:|:-:|
|type|string|string|string|

- 返回值(**json**):
|note|message|result|utc_time|
|:-:|:-:|:-:|:-:|
|e.g.|success|0|017-11-18 05:40:25|
|type|string|int|string|
- 示例:


```
- 示例
{
    "message": "登录成功！",
    "data": {
        "profile": "iot",  #公司名字
        "is_superuser": 1, #超级管理员
        "code_dict": {     #权限列表
            "1": {
                "code_list": [
                    "add",
                    "delete",
                    "update",
                    "get"
                ],
                "id": 1,
                "name": "manager user"
            },
            "2": {
                "code_list": [
                    "post"
                ],
                "id": 2,
                "name": "event"
            },
            "3": {
                "code_list": [
                    "register",
                    "get",
                    "update"
                ],
                "id": 3,
                "name": "manager device"
            },
            "4": {
                "code_list": [
                    "register",
                    "update",
                    "get",
                    "time",
                    "send",
                    "created_today",
                    "delivered_today"
                ],
                "id": 4,
                "name": "order "
            }
        }
    },
    "result": 0
}
```

####失败
```
{
"result": 1
"message": "bad request",
}
```

## 退出登录

`server`: **http://127.0.0.1:8000**
`url`: **/log_out/**

- 请求方法:**POST**


- 返回值(**json**):
- 示例:

```
{
	"result": 0,
	"message": "退出成功"
}
```


## 管理用户
### 增加用户

`server`: **http://127.0.0.1:8000**
`url`: **/users/add/**

- 参数:
|note|email|username|password|is_lock|mobile|temperature_unit|note|
|:-:|:-:|:-:|:-:|
|type|string|string|string||int||string||string|string|

- 返回值(**json**):
- 示例:
```
{
	"result": 0,
	"message": "添加用户成功"
}
```

### 修改用户

`server`: **http://127.0.0.1:8000**
`url`: **/users/update/**

- 请求方法:**POST**
- 参数
|note|email|username|
|:-:|:-:|:-:|:-:|
|type|string|string|
- 返回值(**json**):
- 示例:
```
{
	"result": 0,
	"message": "success"
}
```


### 删除用户

`server`: **http://127.0.0.1:8000**
`url`: **/users/delete/**

- 请求方法:**POST**
- 参数
|note|email|username|
|:-:|:-:|:-:|:-:|
|type|string|string|

- 返回值(**json**):
- 示例
```
{
	"result": 0,
	"message": "success"
}
```


### 查看用户

`server`: **http://127.0.0.1:8000**
`url`: **/users/get/**

- 请求方法:**GET**

- 返回值(**json**):
- 示例:
```
{
    "message": "success",
    "data": {
        "user": {
            "username": "wang",
            "is_lock": false,
            "temperature_unit": null,
            "mobile": "18510234626",
            "profile_id": null,
            "email": "1234@qq.com",
            "note": "",
            "create_time": "2017-12-28T06:31:40.606",
            "password": "9d6472617ff3a524e152c245d6e28aaf41958e28",
            "id": 3
        }
    },
    "result": 0
}
```

##角色操作

###增加角色

`server`: **http://127.0.0.1:8000**
`url`: **/users/add_roles**

- 请求方法:**POST**

- 参数
|note|show_all|
|:-:|:-:|:-:|
|type|string|

- 返回值(**json**):
- 示例
```
{
	"result": 0,
	"message": "success"
}
```

### 修改角色

`server`: **http://127.0.0.1:8000**
`url`: **/users/update_roles**

- 请求方法:**POST**

- 返回值(**json**):
- 示例:


### 查看角色

`server`: **http://127.0.0.1:8000**
`url`: **/users/get_roles**

- 请求方法:**GET**


- 返回值(**json**):
- 示例:
{
	"result": 0,
	"message": "success"
}


## 查看用户操作
#
`server`: **http://127.0.0.1:8000**
`url`: **/users/message/**

- 请求方法:**POST**


- 返回值(**json**):
- 示例:



## 查看公司信息

`server`: **http://127.0.0.1:8000**
`url`: **/users/profile/**

- 请求方法:**POST**

- 返回值(**json**):
- 示例:



### 编辑公司信息

`server`: **http://127.0.0.1:8000**
`url`: **/users/edit_profile/**

- 请求方法:**POST**

- 返回值(**json**):
- 示例:



### １.账号系统  数据库设计
```
Role表：#角色
+----+---------------+---------+-----------------------------+
| id | role          | is_show | create_time                 |
+----+---------------+---------+-----------------------------+
|  1 | administrator |       1 | 2017-12-27 02:33:08.449746  |
|  2 | manager       |       1 | 2017-12-27 02:35:47.443415  |
+----+---------------+---------+-----------------------------+
```

```
User表：用户
+----+----------------------------+-------------+----------+----------+
| id | create_time                | email       | password | username |
+----+----------------------------+-------------+----------+----------+
|  5 | 2017-12-19 08:21:42.133711 | 1234@qq.com | 12345678 | wangwa   |
```

```
users_user_roles：
+----+---------+---------+
| id | user_id | role_id |
+----+---------+---------+
|  1 |       1 |       1 |
|  3 |       2 |       2 |
+----+---------+---------+
```

```
users_iotprofile表：#公司表
+------------+------+--------------+-------------+------------------+-----------------+---------+-----------------+----------------------------+
| profile_id | name | device_field | description | high_temperature | low_temperature | delayed | record_interval | create_time                |
+------------+------+--------------+-------------+------------------+-----------------+---------+-----------------+----------------------------+
| 1          | iot  | 1            | 1           | 1                | 1               |       1 |               1 | 2017-12-27 02:33:08.449746 |
| mm         | mm   | 2            | 3           | 3                | 3               |       3 |               3 | 2017-12-27 02:35:47.443415 |
+------------+------+--------------+-------------+------------------+-----------------+---------+-----------------+----------------------------+
```

```
users_message表： #操作信息
+----+----------------------------+----------+--------------------+---------+
| id | login_time                 | username | message            | user_id |
+----+----------------------------+----------+--------------------+---------+
|  1 | 2017-12-27 02:56:02.196362 | admin    | admin has login in |    NULL |
|  2 | 2017-12-27 02:59:05.448587 | admin    | admin has login in |    NULL |
+----+----------------------------+----------+--------------------+---------+
```
```
users_permissions表： #用户权限
+----+--------------------+------------------------------+-----------------+------------+------+
| id | title              | url                          | code            | menu_gp_id | name |
+----+--------------------+------------------------------+-----------------+------------+------+
|  1 | 增加用户           | /users/add/                  | add             |       NULL | NULL |
|  2 | 删除用户           | /users/delete/               | delete          |       NULL | NULL |
|  3 | 修改用户           | /users/update/               | update          |       NULL | NULL |
|  4 | 查看用户           | /users/get/                  | get             |       NULL | NULL |
|  5 | /event/post/       | /event/post/                 | post            |       NULL | NULL |
```

```
users_permissionsgroup表： #权限组表
+----+----------------+---------+
| id | name           | is_show |
+----+----------------+---------+
|  1 | manager user   |       1 |
|  2 | event          |       1 |
|  3 | manager device |       1 |
|  4 | order          |       1 |
|  5 |  get device    |       1 |
+----+----------------+---------+
```



```
celery==3.1.25
kombu==3.0.37
django-kombu==0.9.4
django-celery==3.2.2
```

