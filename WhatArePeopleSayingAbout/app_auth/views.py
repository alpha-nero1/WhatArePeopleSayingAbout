from app_auth.recaptcha.services.recaptcha_service import validate_recaptcha
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .common.bearer_authentication import CustomBearerAuthentication
from .models import User
from .forms import UserCreationForm
from .serializers import UserSerializer
from .user_backend import UserBackend
from .common.token_utils import get_or_set_token
from app.common.meta_config import get_meta


class Auth(View):
    auth_class = UserBackend()

    # Create your views here.
    def authenticate(self, request, username, password):
        user = self.auth_class.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return True
        return False


class Login(Auth):
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # just so we can send back errors
        if self.authenticate(request, username, password):
            get_or_set_token(username)
            return redirect('/')

        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


class Signup(Auth):
    form_class = UserCreationForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # not saved permanently in db yet

            # clean normalised data.
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # password setting.
            user.set_password(password)

            # register user.
            user.save()

            if self.authenticate(request, email, password):
                return redirect('/')

        return redirect('/')


class UserViewSet(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = User.objects.all().order_by('-created_at')
        serializer = UserSerializer(queryset, many=True)
        content = {
            'users': {
                'data': serializer.data,
                'page': 1,
                'count': len(serializer.data)
            },
            'auth': str(request.auth),
        }
        return Response(content)


class LoginView(Auth):
    template_name = 'app/login.html'

    def get(self, request):
        return render(
            request, 
            self.template_name, 
            { 'meta': get_meta('LoginView') }
        )

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        recaptcha = request.POST.get('g-recaptcha-response')
        valid = validate_recaptcha(recaptcha)
        if (not valid): return redirect('/errors/unverified')
        # just so we can send back errors
        if self.authenticate(request, username, password):
            get_or_set_token(username)
            return redirect('/')
        
        return render(
            request,
            self.template_name,
            {
                'errors': {
                    'authentication': 'Username or password is incorrect.'
                },
                'meta': get_meta('LoginView')
            }
        )


class SignupView(Auth):
    template_name = 'app/signup.html'
    form_class = UserCreationForm

    def get(self, request):
        return render(request, self.template_name, { 'meta': get_meta('SignupView') })

    def post(self, request):
        form = self.form_class(request.POST)
        recaptcha = request.POST.get('g-recaptcha-response')
        valid = validate_recaptcha(recaptcha)
        if (not valid): return redirect('/errors/unverified')
        if form.is_valid():
            user = form.save(commit=False)  # not saved permanently in db yet

            # clean normalised data.
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # password setting.
            user.set_password(password)

            # register user.
            user.save()

            if self.authenticate(request, email, password):
                return redirect('/')
            else:
                return render(
                    request, 
                    self.template_name,
                    {
                        'errors': {
                            'authentication': 'Username or password is incorrect.'
                        },
                        'meta': get_meta('SignupView')
                    }
                )

        return render(
            request, 
            self.template_name,
            {
                'errors': form.errors.get_json_data(),
                'meta': get_meta('SignupView')
            }
        )