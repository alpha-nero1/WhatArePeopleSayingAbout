from app.models import Post
from interactions.models import Comment, PostComment
from interactions.comment.serializers import CommentSerializer
from interactions.comment.forms import CreatePostCommentForm
from rest_framework.permissions import IsAuthenticated
from app_auth.common.bearer_authentication import CustomBearerAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.utils import timezone


class CreatePostComment(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]
    form_class = CreatePostCommentForm

    @parser_classes((JSONParser,)) 
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid() and request.user:
            # Save comment.
            comment = form.save(commit = False)
            comment.user = request.user
            comment.text = request.data['text']
            comment.save()
            # Save post comment link.
            post_comment = PostComment()
            post_comment.post = Post.objects.get(uuid=request.data['post_uuid'])
            post_comment.comment = comment
            post_comment.save()
            serializer = CommentSerializer(instance=comment, context={'user':request.user})
            content = {
                'comment': serializer.data
            }
            return Response(content, 200)

        return Response(None, 422)


class DeletePostComment(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        comment_id = request.data['comment_id']
        try:
            comment = Comment.objects.get(id=comment_id)
            if request.user.id == comment.user.id:
                comment.disabled_at = timezone.now()
                comment.save()
                return Response({ 'data': True }, 200)
        except:
            return Response({ 'error': 'No such comment' }, 403)

        return Response({ 'data': False }, 403)
