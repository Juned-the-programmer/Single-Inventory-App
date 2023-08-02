from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.urls import reverse

class GroupValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude Django admin URLs from group validation
        if not request.path.startswith(reverse('admin:index')):
            # Add your allowed groups here
            allowed_groups = ["Estimate", "GST"]

            if request.user.is_authenticated:
                user_groups = request.user.groups.values_list("name", flat=True)
                if not any(group in user_groups for group in allowed_groups):
                    return HttpResponseForbidden("You don't have permission to access this page.")

        response = self.get_response(request)
        return response