from django.db.models.query_utils import Q
from rest_framework.authtoken.models import Token
from ..models import User


# Get or set a token given a username.
def get_or_set_token(username):
    token = None
    try:
        token = Token.objects.get(Q(user__username=username) | Q(user__email=username))
    except:
        try:
            token = Token.objects.create(user=User.objects.get(Q(username=username) | Q(email=username)))
        except:
            token = ''
    return token
