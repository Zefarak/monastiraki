from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.http.response import JsonResponse


def throw_cookie(request):
    return_obj = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return_obj.set_cookie("gdpr", 'accept')
    return return_obj


def throw_cookie_ajax(request):
    data = {}
    data['gdpr'] = render_to_string(template_name='gdpr/gdpr_ajax.html',
                                    request=request,
                                    context=data
                                    )
    return_obj = JsonResponse(data)
    return_obj.set_cookie("gdpr", 'accept')
    request.session.set_test_cookie()
    return return_obj


def remove_cookie(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.delete_cookie('gdpr')
    return response


class CookiesPolicy(TemplateView):
    template_name = 'gdpr/cookies_policy.html'


class PrivacyPolicy(TemplateView):
    template_name = 'gdpr/pricacy_policy.html'
