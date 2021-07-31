from django.shortcuts import render
from django.views import View
from django.template import RequestContext
import random

def handler404(request, *args, **argv):
    response = render(request, 'app/errors/notfound.html', {})
    response.status_code = 404
    return response


class UnverifiedView(View):
    template_name = 'app/errors/unverified.html'

    def get(self, request):
        return render(request, self.template_name)


class NotFoundView(View):
    template_name = 'app/errors/notfound.html'
    
    def get(self, request):
        rand = random.randint(1, 4)
        notfound_page_class = 'notfound-page-' + str(rand)
        return render(request, self.template_name, { 'notfound_page_class': notfound_page_class })
