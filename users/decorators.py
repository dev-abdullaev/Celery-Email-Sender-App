
from django.shortcuts import redirect, reverse
from functools import wraps
from django.conf import settings
 
 
def login_forbidden(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        u = request.user
        if u.is_authenticated:
            # always return user back to student dashboard
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        return function(request, *args, **kwargs)
 
    return wrap
