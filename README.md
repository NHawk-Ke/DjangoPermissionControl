# DjangoPermissionControl
A reusable app to help you setup the permission control for a Django Website

## Getting Started
### Prerequisites
```
Django version 1.9 or above
```
### Installing

1. Put all the files inside a folder and name it to `permission_control`
2. Replace all `my_project` from the code `from my_project import settings` to be your project name
3. Add the line `FuncToPerms = {}` at the end of your `settings.py`. Also, add `permission_control` to your `INSTALLED_APP` inside `settings.py`
4. Drag this folder to the same directory as `manage.py`

## How To Use
The main logic is inside the three json file 
```
PermList.json
GroupToPerm.json
FuncToPerm.json
```
1. Add `DjangoPermissionControl` to `INSTALLED_APPS` in `settings.py`
```
INSTALLED_APPS = [
    ......
    'DjangoPermissionControl',
    ......
]
```
2. Edit the three json files
3. Run the command `python manage.py setuppermissions` to setup properly.
4. Inside your `views.py` add the line `from permission_control import PermissionControlMixin`
5. For each function-based view that you want to have permission add `@PermissionControlMixin.check_permission()` on top as decorator
6. For each class-based view just inherited `PermissionControlMixin`
7. Make sure you have `login_required` before the permission decorator takes place. e.g.
```
@login_required(login_url=login_url)
@PermissionControlMixin.check_permission()
def example_view(request):
    ...
or
class ExampleView(LoginRequiredMixin, PermissionControlMixin, FormView):
    ...
```

Just add users to group for larger use.
Once you finished all the steps described above you are good to go.

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
P.S.: The format of this string does not matter

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
As you can see this file maps all the permissions to groups. You can just edit this files without worrying weather the group is there or not. The app will take care of that. It will only create group if it is not there and will never delete a existing group. To delete an existing group, you have to do it manually.

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
The app will use this file to check weather a certain user has the permission to access a function or not. This is your responsibility to update this file, if you update a function name or changed a permission name.
P.S.: If you do not have a namespace, just leave it empty. e.g.(".my_function1"). This time the dot does matter.



