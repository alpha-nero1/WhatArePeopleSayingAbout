from django.shortcuts import render
from django.views import View
from django.template import RequestContext
import random

def handler404(request, *args, **argv):
    rand = random.randint(1, 4)
    notfound_page_class = 'notfound-page-' + str(rand)
    template_name = 'app/errors/notfound.html'
    response = render(
        request, 
        template_name, 
        { 'notfound_page_class': notfound_page_class }
    )
    response.status_code = 404
    return response


class UnverifiedView(View):
    template_name = 'app/errors/unverified.html'

    def get(self, request):
        return render(request, self.template_name)


class NotFoundView(View):
    template_name = 'app/errors/notfound.html'
    
    def get(self, request):
        return handler404(request)
