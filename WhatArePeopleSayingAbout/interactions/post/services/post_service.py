from app.common.constants import CONSTANTS
from app.models import Post, Topic
from django.db.models import Q

def get_posts_queryset(topic, post_uuid = None):
    posts = Post.objects.filter(topic__kebab_name=topic, disabled_at__isnull=True)
    if (post_uuid is not None):
        posts = posts.exclude(uuid=post_uuid)
    return posts.order_by('-created_at')

def get_search_posts_queryset(term):
    # Note: In future make search more elaborate.
    topics = Post.objects.filter(Q(text__icontains=term) | Q(user__username__icontains=term)).order_by('-created_at')[:CONSTANTS.get('POSTS').get('MAX_SEARCH_SIZE') + 1]
    return topics
