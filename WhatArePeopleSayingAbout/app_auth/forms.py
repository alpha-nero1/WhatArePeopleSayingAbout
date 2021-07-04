from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


## Custom user creation form so we can check
## form validity
class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(required=True, min_length=3)

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args,**kargs)

    class Meta:
        model = User

        ## all the fields deeming the form valid
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
