import os
import json
from django.core.management.base import BaseCommand, CommandError
from my_project import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group


class Command(BaseCommand):

    help = 'Add a new or existing permission to a list of group. The format should be: python manage.py ' \
           'addpermtogroup permission_name ["group_1","group_2"]                 FuncToPerm variable is not updated. ' \
           'Please manuely edit. '

    def add_arguments(self, parser):
        parser.add_argument('permission', type=str) 
        parser.add_argument('group list', type=str)

    def handle(self, *args, **kwargs):
        perm_name = kwargs.get('permission')
        group_name = kwargs.get('group list').strip('[]').replace('"', '').replace("'", '').split(',')
        ct, created = ContentType.objects.get_or_create(
            model="GlobalPermission", app_label="global_permission"
        )
        try:
            for group in group_name:
                Group.objects.get(name=group)
        except Exception as err:
            raise CommandError("The Group %s doe not exist" % group)
        
        perm, created = Permission.objects.get_or_create(codename=perm_name, name=perm_name, content_type=ct)
        
        # create new permission
        for group in group_name:
            if perm not in Group.objects.get(name=group).permissions.all():
                Group.objects.get(name=group).permissions.add(perm)

        GROUP_PATH = os.path.join(settings.BASE_DIR, 'md_permission/GroupToPerm.json')
        PERM_PATH = os.path.join(settings.BASE_DIR, 'md_permission/PermList.json')

        # reset GroupToPerm.json
        with open(GROUP_PATH, "r") as json_file:
            file_2 = json.load(json_file)
        for group in group_name:
            if perm_name not in file_2[group]:
                file_2[group].append(perm_name)
        with open(GROUP_PATH, "w") as json_file:
            json.dump(file_2, json_file, indent=4)

        # reset PermList.json
        with open(PERM_PATH, "r") as json_file:
            file_3 = json.load(json_file)
        if perm_name not in file_3:
            file_3.append(perm_name)
        with open(PERM_PATH, "w") as json_file:
            json.dump(file_3, json_file, indent=4)
