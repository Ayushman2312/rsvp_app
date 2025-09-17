from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import PhoneSubmission
# Create your views here.
class HomeView(TemplateView):
    def get_template_names(self):
        if is_mobile(self.request):
            return ["mobile.html"]
        return ["page.html"]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def is_mobile(request):
    """Detect if the request is coming from a mobile device"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone' , 'windows phone']
    return any(keyword in user_agent for keyword in mobile_keywords)


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
@require_POST
def save_phone(request):
    phone = (request.POST.get('phone') or '').strip()
    # Basic validation: keep 10-15 digits
    digits = ''.join([c for c in phone if c.isdigit()])
    if len(digits) < 10 or len(digits) > 15:
        return HttpResponseBadRequest('Invalid phone')

    PhoneSubmission.objects.create(
        phone=phone,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        path=request.path,
        referrer=request.META.get('HTTP_REFERER', ''),
        ip_address=_get_client_ip(request),
    )
    return JsonResponse({'ok': True})