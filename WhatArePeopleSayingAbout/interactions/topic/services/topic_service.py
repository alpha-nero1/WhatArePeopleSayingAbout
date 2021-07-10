from django.db.models.aggregates import Sum
from app.common.constants import CONSTANTS
from django.db.models.expressions import OuterRef
from app.models import Post, Topic
from django.db.models import Count, Subquery
from django.utils import timezone
from datetime import datetime, timedelta


def get_or_set_topic(topic_name):
    # Normailsed kebab name!
    kebab_name = topic_name.lower().replace(' ', '-')
    # Get or save topic
    try:
        existing_topic = Topic.objects.get(kebab_name=kebab_name, disabled_at__isnull=True)
        return existing_topic
    except:
        topic = Topic(name=topic_name, kebab_name=kebab_name)
        topic.save()
        return topic


# Gets the topics with the most posts created for them in
# the past 7 days!
def get_trending_topics_queryset():
    week_ago = (timezone.now() - timedelta(days=CONSTANTS.get('TOPICS').get('TRENDING_OFFSET_DAYS')))
    topics = (
        Topic.objects
        .filter(disabled_at__isnull=True)
        # Note: fix this!
        .annotate(
            posts=Subquery(
                Post.objects.filter(
                    topic__id=OuterRef('id'),
                    created_at__gt=week_ago,
                    disabled_at__isnull=True
                ).values('id')
            ),
            num_posts=Count('posts')
        )
        .order_by('-num_posts', '-created_at')
    )
    return topics


def get_search_topics_queryset(topic_name):
    # Note: In future make search more elaborate.
    topics = Topic.objects.filter(name__icontains=topic_name).order_by('-created_at')[:CONSTANTS.get('TOPICS').get('MAX_SEARCH_SIZE') + 1]
    return topics