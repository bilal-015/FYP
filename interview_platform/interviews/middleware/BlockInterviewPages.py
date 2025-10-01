from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlparse

class BlockAfterCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only those views should be blocked
        blocked_paths = [
            reverse('mcqs_page'),
            reverse('coding_page'),
            reverse('confidence_score_page'),
            # Don't reverse interview_report because it needs an argument
        ]

        # Allow static/media requests
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        if request.session.get("interview_Completed") is True:
            normalized_path = urlparse(request.path).path.rstrip('/')
            normalized_blocked = [urlparse(p).path.rstrip('/') for p in blocked_paths]

            # Special case: block ANY /interview_report/<id>/ path
            if normalized_path in normalized_blocked or normalized_path.startswith("/interview_report/"):
                return redirect('dashboard')

        return self.get_response(request)
