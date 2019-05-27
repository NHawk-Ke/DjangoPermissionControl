import os
import json
from django.core.management.base import BaseCommand, CommandError
from my_project import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
import textwrap


class Command(BaseCommand):

    help = 'Delete a permission'

    def add_arguments(self, parser):
        parser.add_argument('permission', type=str) 

    def handle(self, *args, **kwargs):
        perm_name = kwargs.get('permission')
        ct, created = ContentType.objects.get_or_create(
            model="GlobalPermission", app_label="global_permission"
        )
        try:
            perm = Permission.objects.get(codename=perm_name, name=perm_name, content_type=ct)
        except Exception as err:
            raise CommandError("The Permission %s doe not exist" % perm)

        FUNC_PATH = os.path.join(settings.BASE_DIR, 'md_permission/FuncToPerm.json')
        GROUP_PATH = os.path.join(settings.BASE_DIR, 'md_permission/GroupToPerm.json')
        PERM_PATH = os.path.join(settings.BASE_DIR, 'md_permission/PermList.json')

        # reset FuncToPerm.json
        with open(FUNC_PATH, "r") as json_file:
            file_1 = json.load(json_file)
        for key in file_1:
            for index, item in enumerate(file_1[key]):
                if item == perm_name:
                    if len(file_1[key]) == 1:
                        del file_1[key]
                    else:
                        del file_1[key][index]
        with open(FUNC_PATH, "w") as json_file:
            json.dump(file_1, json_file, indent=4)        

        # reset GroupToPerm.json
        with open(GROUP_PATH, "r") as json_file:
            file_2 = json.load(json_file)
        for group in file_2:
            for index, name in file_2[group]:
                if name == perm_name:
                    del file_2[group][index]
        with open(GROUP_PATH, "w") as json_file:
            json.dump(file_2, json_file, indent=4)

        # reset PermList.json
        with open(PERM_PATH, "r") as json_file:
            file_3 = json.load(json_file)
        for index, name in enumerate(file_3):
            if name == perm_name:
                del file_3[index]
        with open(PERM_PATH, "w") as json_file:
            json.dump(file_3, json_file, indent=4)

        # update FuncToPerm variable
        settings.FuncToPerm = file_1
