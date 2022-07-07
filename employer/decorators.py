from django.contrib import messages
from django.shortcuts import redirect


def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "your must login")
            return redirect("signin")

    return wrapper
