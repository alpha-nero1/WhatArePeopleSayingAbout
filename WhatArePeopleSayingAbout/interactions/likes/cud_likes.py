
from django.utils import timezone
from app.models import Post
from interactions.models import CommentDislike, CommentLike, PostDislike, PostLike
from app_auth.common.bearer_authentication import CustomBearerAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


## Post likes.
class CreatePostLike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def remove_dislike(self, post_uuid, user_id):
        try:
            dislike = PostDislike.objects.get(user_id=user_id, post__uuid=post_uuid, disabled_at=None)
            dislike.disabled_at = timezone.now()
            dislike.save()
            return True
        except:
            return False

    def get_or_set_like(self, post_uuid, user_id):
        like = None
        post = Post.objects.get(uuid=post_uuid)
        try:
            like = PostLike.objects.get(user_id=user_id, post=post, disabled_at=None)
        except:
            # No like exists, create it.
            like = PostLike(post=post, user_id=user_id)
            like.save()
        return like
        
    def post(self, request):
        post_uuid = request.data['post_uuid']
        user_id = request.user.id
        pl = self.get_or_set_like(post_uuid, user_id)
        did_action = self.remove_dislike(post_uuid, user_id)
        if (pl):
            return Response(did_action, 200)
        return Response('Could not like post.', 500)


class DeletePostLike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_uuid = request.data['post_uuid']
        user_id = request.user.id
        try:
            post_like = PostLike.objects.get(post__uuid=post_uuid, user_id=user_id, disabled_at=None)
            now = timezone.now()
            post_like.updated_at = now
            post_like.disabled_at = now
            post_like.save()
            return Response(True, 200)
        except Exception as e:
            return Response('Could not unlike post', 500)


class CreatePostDislike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def remove_like(self, post_uuid, user_id):
        try:
            like = PostLike.objects.get(user_id=user_id, post__uuid=post_uuid, disabled_at=None)
            like.disabled_at = timezone.now()
            like.save()
            return True
        except:
            return False
    
    def get_or_set_dislike(self, post_uuid, user_id):
        dislike = None
        post = Post.objects.get(uuid=post_uuid)
        try:
            dislike = PostDislike.objects.get(user_id=user_id, post=post, disabled_at=None)
        except:
            # No like exists, create it.
            dislike = PostDislike(post=post, user_id=user_id)
            dislike.save()
        return dislike
        
    def post(self, request):
        post_uuid = request.data['post_uuid']
        user_id = request.user.id
        pdl = self.get_or_set_dislike(post_uuid, user_id)
        did_action = self.remove_like(post_uuid, user_id)
        if (pdl):
            return Response(did_action, 200)
        return Response('Could not dislike post.', 500)


class DeletePostDislike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_uuid = request.data['post_uuid']
        user_id = request.user.id
        try:
            post_dislike = PostDislike.objects.get(post__uuid=post_uuid, user_id=user_id, disabled_at=None)
            now = timezone.now()
            post_dislike.updated_at = now
            post_dislike.disabled_at = now
            post_dislike.save()
            return Response(True, 200)
        except:
            return Response('Could not undislike post', 500)


## Comment likes.
class CreateCommentLike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def remove_dislike(self, comment_id, user_id):
        try:
            dislike = CommentDislike.objects.get(user_id=user_id, comment_id=comment_id, disabled_at=None)
            dislike.disabled_at = timezone.now()
            dislike.save()
            return True
        except:
            return False

    def get_or_set_like(self, comment_id, user_id):
        like = None
        try:
            like = CommentLike.objects.get(user_id=user_id, comment_id=comment_id, disabled_at=None)
        except:
            # No like exists, create it.
            like = CommentLike(comment_id=comment_id, user_id=user_id)
            like.save()
        return like
        
    def post(self, request):
        comment_id = request.data['comment_id']
        user_id = request.user.id
        cl = self.get_or_set_like(comment_id, user_id)
        did_action = self.remove_dislike(comment_id, user_id)
        if (cl):
            return Response(did_action, 200)
        return Response('Could not like comment.', 500)


class DeleteCommentLike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        comment_id = request.data['comment_id']
        user_id = request.user.id
        try:
            comment_like = CommentLike.objects.get(comment_id=comment_id, user_id=user_id, disabled_at=None)
            now = timezone.now()
            comment_like.updated_at = now
            comment_like.disabled_at = now
            comment_like.save()
            return Response(True, 200)
        except:
            return Response('Could not unlike comment', 500)


class CreateCommentDislike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def remove_like(self, comment_id, user_id):
        try:
            like = CommentLike.objects.get(user_id=user_id, comment_id=comment_id, disabled_at=None)
            like.disabled_at = timezone.now()
            like.save()
            return True
        except:
            return False

    def get_or_set_dislike(self, comment_id, user_id):
        dislike = None
        try:
            dislike = CommentDislike.objects.get(user_id=user_id, comment_id=comment_id, disabled_at=None)
        except:
            # No like exists, create it.
            dislike = CommentDislike(comment_id=comment_id, user_id=user_id)
            dislike.save()
        return dislike
        
    def post(self, request):
        comment_id = request.data['comment_id']
        user_id = request.user.id
        cdl = self.get_or_set_dislike(comment_id, user_id)
        did_action = self.remove_like(comment_id, user_id)
        if (cdl):
            return Response(did_action, 200)
        return Response('Could not dislike comment.', 500)


class DeleteCommentDislike(APIView):
    authentication_classes = [CustomBearerAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        comment_id = request.data['comment_id']
        user_id = request.user.id
        try:
            comment_dislike = CommentDislike.objects.get(comment_id=comment_id, user_id=user_id, disabled_at=None)
            now = timezone.now()
            comment_dislike.updated_at = now
            comment_dislike.disabled_at = now
            comment_dislike.save()
            return Response(True, 200)
        except:
            return Response('Could not undislike post', 500)
