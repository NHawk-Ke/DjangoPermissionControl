# DjangoPermissionControl
A reuseable app to help you setup the permission control for a Django Website

## Getting Started
### Prerequisites
```
Django version 1.9 or above
```
### Installing

1. Put all the files inside a folder and name it to `permission_control`
2. Replace all `my_project` from the code `from my_project import settings` to be your project name
3. Add the line `FuncToPerms = {}` at the end of your `settings.py`. Also, add `permission_control` to your `INSTALLED_APP` inside `settings.py`

## How To Use
The main logic is inside the three json file 
```
PermList.json
GroupToPerm.json
FuncToPerm.json
```

### PermList.json
```
[
    "Custom.permission.name1",
    "Custom.permission.name2",
    "Custom.permission.name3",
    "Custom.permission.name4"
]
```
This file contains all the permissions that you want to use to check permissions for a user. You can add as many as you want. The app will dynamically create or delete permissions according to this file.

### GroupToPerm.json
```
{
    "Group Name1": [
        "Custom.permission.name1",
		"Custom.permission.name2",
    ],
    "Group Name2": [
		"Custom.permission.name3",
		"Custom.permission.name4",
    ]
}
```
As you can see this file maps all the permissions to groups. You can just edit this files without warrying weather the group is there or not. The app will take care of that. It will only create group if it is not there and will never delete a existing group. To delete an exsisting group, you have to do it manully.

### FuncToPerm.json
```
{

    "namespace.FuncName1": [
        "Custom.permission.name1",
        "Custom.permission.name2"
    ],
    "namespace.FuncName2": [
        "Custom.permission.name3"
    ],
    "namespace2.FuncName1": [
        "Custom.permission.name3"
    ],
    "namespace.FuncName3": [
		    "Custom.permission.name4"
    ]
}
```
The app will use this file to check weather a certain user has the permission to access a function or not. This is your resposibility to update this file, if you update a function name or changed a permission name.
