import os
import json
from django.core.management.base import BaseCommand, CommandError
from my_project import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group


class Command(BaseCommand):
    help = "replace an old permission with a new one. Potential args: old_permission, new_permission"
    
    def add_arguments(self, parser):
        parser.add_argument('old permission', type=str)
        parser.add_argument('new permission', type=str)

    def handle(self, *args, **kwargs):
        old_name = kwargs.get('old permission')
        new_name = kwargs.get('new permission')
        ct, created = ContentType.objects.get_or_create(
            model="GlobalPermission", app_label="global_permission"
        )
        try:
            old_perm = Permission.objects.get(codename=old_name, name=old_name, content_type=ct)
        except Exception as err:
            raise CommandError('The old permission "%s" does not exist' % old_name)
        if old_name == new_name:
            raise CommandError('The old name "%s" and the new name "%s" are the same' % (old_name, new_name))

        # create new permission
        new_perm, created = Permission.objects.get_or_create(codename=new_name, name=new_name, content_type=ct)
        for group in Group.objects.all():
            if old_perm in group.permissions.all():
                group.permissions.remove(old_perm)
                group.permissions.add(new_perm)
        old_perm.delete()

        FUNC_PATH = os.path.join(settings.BASE_DIR, 'md_permission/FuncToPerm.json')
        GROUP_PATH = os.path.join(settings.BASE_DIR, 'md_permission/GroupToPerm.json')
        PERM_PATH = os.path.join(settings.BASE_DIR, 'md_permission/PermList.json')
        
        # reset FuncToPerm.json
        with open(FUNC_PATH, "r") as json_file:
            file_1 = json.load(json_file)
        for keys in file_1:
            for index, item in enumerate(file_1[keys]):
                if item == old_name:
                    file_1[keys][index] = new_name
        with open(FUNC_PATH, "w") as json_file:
            json.dump(file_1, json_file, indent=4)

        # reset GroupToPerm.json
        with open(GROUP_PATH, "r") as json_file:
            file_2 = json.load(json_file)
        for keys in file_2:
            for index, item in enumerate(file_2[keys]):
                if item == old_name:
                    file_2[keys][index] = new_name
        with open(GROUP_PATH, "w") as json_file:
            json.dump(file_2, json_file, indent=4)

        # reset PermList.json
        with open(PERM_PATH, "r") as json_file:
            file_3 = json.load(json_file)
        for index, item in enumerate(file_3):
            if item == old_name:
                file_3[index] = new_name
        with open(PERM_PATH, "w") as json_file:
            json.dump(file_3, json_file, indent=4)

        # update FuncToPerm variable
        with open(FUNC_PATH, 'r') as json_file:
            settings.FuncToPerm = json.load(json_file)
