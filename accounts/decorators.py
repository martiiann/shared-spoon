from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    """
    Decorator for views that checks that the logged-in user
    is marked as is_admin=True on the custom User model.
    """
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not (user.is_authenticated and getattr(user, 'is_admin', False)):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped
