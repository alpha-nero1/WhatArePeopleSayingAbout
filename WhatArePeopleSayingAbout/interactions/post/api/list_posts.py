from app.common.constants import CONSTANTS
from interactions.post.services.post_service import get_posts_queryset
from app_auth.common.bearer_authentication import CustomBearerAuthentication
from interactions.post.serializers import PostSerializer
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PostsResultsSetPagination(PageNumberPagination):
    page_size = CONSTANTS.get('POSTS').get('PAGE_SIZE')
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ListPosts(mixins.ListModelMixin, GenericAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsResultsSetPagination
    authentication_classes = []
    queryset = None

    def get (self, request):
        topic = request.GET.get('topic')
        post_uuid = request.GET.get('post_uuid')

        if (topic):
            self.queryset = self.filter_queryset(
                # Use the standard queryset from the service.
                get_posts_queryset(topic, post_uuid)
            )
            page = self.paginate_queryset(self.get_queryset())

            if (page is not None):
                serializer = PostSerializer(instance=page, context={'user':request.user}, many=True)
                return self.get_paginated_response(serializer.data)

            return Response({ 'data': {} }, 200)
        return Response(None, 400)