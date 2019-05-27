import os
import json
from django.core.management.base import BaseCommand
from my_project import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group


class Command(BaseCommand):
    help = "Automatically manage permissions configuration from md_permission/FuncToPerm.json, GroupToPerm.json, " \
           "and PermList.json "

    def handle(self, *args, **kwargs):
        ct, created = ContentType.objects.get_or_create(
            model="GlobalPermission", app_label="global_permission"
        )
        FUNC_PATH = os.path.join(settings.BASE_DIR, 'md_permission/FuncToPerm.json')
        GROUP_PATH = os.path.join(settings.BASE_DIR, 'md_permission/GroupToPerm.json')
        PERM_PATH = os.path.join(settings.BASE_DIR, 'md_permission/PermList.json')
        
        # set FuncToPermission
        with open(FUNC_PATH, 'r') as json_file:
            settings.FuncToPerms = json.load(json_file)

        # clear old permissions and add new permissions from PermList.json
        ct_perm = Permission.objects.filter(content_type=ct)
        if ct_perm:
            ct_perm.delete()
        with open(PERM_PATH, 'r') as json_file:
            permission_list = json.load(json_file)
        for permission in permission_list:
            Permission.objects.create(codename=permission, name=permission, content_type=ct)
        
        # reset group permissions
        with open(GROUP_PATH, 'r') as json_file:
            group_permissions = json.load(json_file)
        for name in group_permissions:
            group, created = Group.objects.get_or_create(name=name)
            group_perms = []
            for perm in group_permissions[name]:
                group_perms.append(Permission.objects.get(codename=perm, name=perm, content_type=ct))
            group.permissions.set(group_perms)



