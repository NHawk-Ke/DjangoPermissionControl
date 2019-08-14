import os
import json
from django.apps import AppConfig
from django.http import Http404
from my_project import settings
from django.shortcuts import redirect


class PermissionControlMixin(object):

    def initialize_permissions():
        DATA_PATH = os.path.join(settings.BASE_DIR, 'DjangoPermissionControl/FuncToPerm.json')
        with open(DATA_PATH, 'r') as json_file:
            settings.FuncToPerms = json.load(json_file)

    def check_permission():
        def decorator(func):
            def wrapper(request, *args, **kwargs):
                # The two line below can be removed if login_required decorator is already used
                if not request.user.is_authenticated:
                    return redirect("login")
                
                # Check if the system has loaded all permissions
                if not settings.FuncToPerms:
                    PermissionControlMixin.initialize_permissions()
                app_name = request.resolver_match.app_name
                try:
                    for Perm in settings.FuncToPerms[app_name+"."+func.__name__]:
                        if not request.user.has_perm('global_permission.'+Perm):
                            raise Http404("You dont have permission: " + Perm)
                except KeyError as e:
                    error_msg = "Key Error: " + str(e.args) + "\nThis permission name is not found in FuncToPerms."
                    error_msg += "\nPlease Check the json file and set permission again."
                    raise Http404(error_msg)

                return func(request=request, *args, **kwargs)
            return wrapper
        return decorator

    def permission_check(self, user, request):
        if not settings.FuncToPerms:
            PermissionControlMixin.initialize_permissions()
        try:
            app_name = request.resolver_match.app_name
            for Perm in settings.FuncToPerms[app_name+"."+self.__class__.__name__]:
                if not user.has_perm('global_permission.'+Perm):
                    raise Http404("You don't have permission: " + Perm)
        except KeyError as e:
            error_msg = "Key Error: " + str(e.args) + "\nThis permission name is not found in FuncToPerms."
            error_msg += "\nPlease Check the json file and set permission again."
            raise Http404(error_msg)
        return True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if self.permission_check(request.user, request):
            return super(PermissionControlMixin, self).dispatch(request, *args, **kwargs)

