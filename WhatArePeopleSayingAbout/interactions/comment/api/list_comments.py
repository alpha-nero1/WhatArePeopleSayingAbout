from app.common.constants import CONSTANTS
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from interactions.comment.serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from interactions.models import Comment

class CommentsResultsSetPagination(PageNumberPagination):
    page_size = CONSTANTS.get('COMMENTS').get('PAGE_SIZE')
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ListPostComments(mixins.ListModelMixin, GenericAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentsResultsSetPagination
    authentication_classes = []
    queryset = None

    def get(self, request):
        post_uuid = request.GET.get('post_uuid')

        if (post_uuid):
            self.queryset = self.filter_queryset(
                Comment.objects
                .select_related('user')
                .filter(
                    postcomment__post__uuid=post_uuid, disabled_at=None
                ).order_by('created_at')
            )
            page = self.paginate_queryset(self.get_queryset())
            if (page is not None):
                serializer = CommentSerializer(instance=page, context={'user':request.user}, many=True)
                return self.get_paginated_response(serializer.data)

            return Response({ 'data': {} }, 200)

        return Response(None, 400)