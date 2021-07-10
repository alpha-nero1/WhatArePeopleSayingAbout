from app.common.constants import CONSTANTS
from app.models import Post, Topic
from app_auth.serializers import UserSerializer
from app_auth.models import User
from rest_framework import serializers
from django.utils.timesince import timesince

class PostTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = [
            'id',
            'name',
            'kebab_name'
        ]

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    topic = PostTopicSerializer(read_only=True)
    # Header just made from start of text.
    header = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    naturaltime = serializers.SerializerMethodField()
    header_size = CONSTANTS.get('POSTS').get('HEADER_SIZE')

    class Meta:
        model = Post
        fields = [
            'id', 
            'text', 
            'user', 
            'uuid', 
            'created_at', 
            'updated_at', 
            'total_likes',
            'is_liked',
            'is_disliked',
            'topic',
            'header',
            'naturaltime'
        ]

    def get_naturaltime(self, obj):
        time = timesince(obj.created_at)
        return time

    def get_header(self, obj):
        header = obj.text
        if (len(header) > self.header_size): header = header[0: self.header_size] + '...'
        return header

    def get_total_likes(self, obj):
        return (
            obj.postlike_set.filter(disabled_at__isnull=True).count() - 
            obj.postdislike_set.filter(disabled_at__isnull=True).count()
        )

    def get_is_liked(self, obj):
        return obj.postlike_set.filter(user_id=self.context.get('user').id, disabled_at__isnull=True).count() > 0

    def get_is_disliked(self, obj):
        return obj.postdislike_set.filter(user_id=self.context.get('user').id, disabled_at__isnull=True).count() > 0
         

