# myapp/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that can be accessed without logging in
        allowed_paths = [
            reverse('login'),
            reverse('candidateLogin'),
            reverse('register'),
            reverse('register_candidate'),
            reverse('forgotPassword'),
            reverse('get_all_emails'),
            reverse('send_verification_code'),
            reverse('set_new_password'),
            reverse('send_email_verification'),
            reverse('admin:index'),
        ]

        # Allow static/media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # If session key is missing AND path is not in allowed list → redirect
        if not (request.session.get("candidate_id") or request.session.get("admin_id")) and request.path not in allowed_paths:
            return redirect('login')

        return self.get_response(request)
