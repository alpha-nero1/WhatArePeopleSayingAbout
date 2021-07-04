from .models import User
from django.db.models import Q

## Custom user email login backend to replace
## the standard django one
class UserBackend(object):

    # Required method 1
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(username=username) | Q(email=username)).order_by('id').first()
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    # Required method 2
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesnotExist:
            return None