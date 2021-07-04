from interactions.topic.services.topic_service import get_or_set_topic
from interactions.post.serializers import PostSerializer
from app.models import Post
from interactions.models import Comment, PostComment
from interactions.comment.serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from app_auth.common.bearer_authentication import CustomBearerAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.utils import timezone


class CreatePost(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    @parser_classes((JSONParser,)) 
    def post(self, request):
        text = request.data['text']
        topic_name = request.data['topic']
        if request.user and text and topic_name:
            topic = get_or_set_topic(topic_name)
            # Save post.
            post = Post(topic=topic, text=text, user=request.user)
            post.save()
            serializer = PostSerializer(instance=post, context={'user':request.user})
            content = {
                'post': serializer.data
            }
            return Response(content, 200)

        return Response(None, 422)


class DeletePost(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        uuid = request.data['uuid']
        try:
            post = Post.objects.get(uuid=uuid)
            if request.user.id == post.user.id:
                post.disabled_at = timezone.now()
                post.save()
                return Response({ 'data': True }, 200)
        except:
            return Response({ 'error': 'No such comment' }, 403)

        return Response({ 'data': False }, 403)
