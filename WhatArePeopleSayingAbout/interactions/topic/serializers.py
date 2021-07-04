from interactions.post.serializers import PostSerializer
from app.models import Topic
from rest_framework import serializers

class TopicSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    total_posts = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = [
            'id',
            'name',
            'post',
            'kebab_name',
            'total_posts'
        ]

    def get_total_posts(self, obj):
        return (obj.post_set.filter(disabled_at__isnull=True).count())