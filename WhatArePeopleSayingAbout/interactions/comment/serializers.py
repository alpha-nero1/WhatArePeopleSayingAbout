from app_auth.serializers import UserSerializer
from app_auth.models import User
from ..models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_likes = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 
            'text', 
            'user', 
            'parent', 
            'created_at', 
            'updated_at', 
            'total_likes',
            'is_liked',
            'is_disliked'
        ]

    def get_total_likes(self, obj):
        return (
            obj.commentlike_set.filter(disabled_at__isnull=True).count() - 
            obj.commentdislike_set.filter(disabled_at__isnull=True).count()
        )

    def get_is_liked(self, obj):
        return obj.commentlike_set.filter(user_id=self.context.get('user').id, disabled_at__isnull=True).count() > 0

    def get_is_disliked(self, obj):
        return obj.commentdislike_set.filter(user_id=self.context.get('user').id, disabled_at__isnull=True).count() > 0
         

