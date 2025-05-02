from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    """
    Decorator for views that checks that the logged-in user
    is a superuser.
    """
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not (user.is_authenticated and user.is_superuser):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped
