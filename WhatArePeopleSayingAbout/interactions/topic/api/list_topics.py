from interactions.topic.services.topic_service import get_search_topics_queryset, get_trending_topics_queryset
from interactions.topic.serializers import TopicSerializer
from app.common.constants import CONSTANTS
from app_auth.common.bearer_authentication import CustomBearerAuthentication
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TopicsResultsSetPagination(PageNumberPagination):
    page_size = CONSTANTS.get('TOPICS').get('PAGE_SIZE')
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ListTrendingTopics(mixins.ListModelMixin, GenericAPIView):
    serializer_class = TopicSerializer
    pagination_class = TopicsResultsSetPagination
    authentication_classes = []
    queryset = None

    def get (self, request):
        self.queryset = self.filter_queryset(
            # Use the standard queryset from the service.
            get_trending_topics_queryset()
        )
        page = self.paginate_queryset(self.get_queryset())

        if (page is not None):
            serializer = TopicSerializer(instance=page, context={'user':request.user}, many=True)
            return self.get_paginated_response(serializer.data)

        return Response({ 'data': {} }, 200)


class SearchTopics(mixins.ListModelMixin, GenericAPIView):
    serializer_class = TopicSerializer
    pagination_class = TopicsResultsSetPagination
    authentication_classes = []
    queryset = None

    def get(self, request):
        topic = request.GET.get('topic')
        if (topic):
            self.queryset = self.filter_queryset(
                # Use the standard queryset from the service.
                get_search_topics_queryset(topic)
            )
            page = self.paginate_queryset(self.get_queryset())

            if (page is not None):
                serializer = TopicSerializer(instance=page, context={'user':request.user}, many=True)
                return self.get_paginated_response(serializer.data)

            return Response({ 'data': {} }, 200)
        return Response(None, 400)