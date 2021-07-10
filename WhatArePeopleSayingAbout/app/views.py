from app_auth.recaptcha.services.recaptcha_service import validate_recaptcha
from django.conf import settings
from interactions.topic.serializers import TopicSerializer
from interactions.post.serializers import PostSerializer
from app.common.constants import CONSTANTS
from interactions.post.services.post_service import get_posts_queryset, get_search_posts_queryset
from interactions.topic.services.topic_service import get_or_set_topic, get_search_topics_queryset, get_trending_topics_queryset
from app_auth.common.token_utils import get_or_set_token
from django.shortcuts import render, redirect

from django.views import View
from .models import User, Topic, Post


def handle_view_post(request):
    topic_name = request.POST.get('topic')
    recaptcha = request.POST.get('g-recaptcha-response')
    valid = validate_recaptcha(recaptcha)
    if (valid):
        topic = get_or_set_topic(topic_name)
        user = request.user if request.user.username else None
        new_post = Post(topic=topic, text=request.POST.get('text'), user=user)
        new_post.save()
        # Create the post and redirect to new post page.
        return redirect('/topics/' + topic.kebab_name + '/' + str(new_post.uuid))
    return redirect('/errors/unverified/')


class HomeView(View):
    template_name = 'app/home.html'
    next_page = False

    def get(self, request):
        page_size = CONSTANTS.get('TOPICS').get('PAGE_SIZE')
        topics = get_trending_topics_queryset()[:(page_size + 1)]
        if (len(topics) > page_size):
            # There is a next page!
            self.next_page = True
            topics = topics[0:(len(topics) - 1)]
        
        serializer = TopicSerializer(instance=topics, context={'user':request.user}, many=True)
        response = render(
            request,
            self.template_name,
            {
                'topics': serializer.data,
                'user': request.user,
                'next_page': self.next_page
            }
        )

        # Configure wndpoint for scripts to use...
        response.set_cookie('endpoint_url', settings.ENDPOINT_URL)
        if (request.user.username):
            response.set_cookie('auth_token', get_or_set_token(request.user.username))
        else:
            response.delete_cookie('auth_token')
        return response


    def post(self, request):
        return handle_view_post(request)


class TopicView(View):
    template_name = 'app/topic.html'
    next_page = False

    def get(self, request, id):
        topic = Topic.objects.get(kebab_name = id)
        posts = get_posts_queryset(id)
        # First posts page!
        posts = posts[:(CONSTANTS.get('POSTS').get('PAGE_SIZE') + 1)]
        if (len(posts) > CONSTANTS.get('POSTS').get('PAGE_SIZE')):
            self.next_page = True
            # There is a next page!
            posts = posts[0:(len(posts) - 1)]

        serializer = PostSerializer(instance=posts, context={'user':request.user}, many=True)
        return render(
            request, 
            self.template_name,
            {
                'topic': topic,
                'posts': serializer.data,
                'user': request.user,
                'next_page': self.next_page
            }
        )

    def post(self, request, id):
        return handle_view_post(request)


class PostView(View):
    template_name = 'app/post.html'

    def get(self, request, id):
        post = Post.objects.get(uuid=id)
        main_post_serializer = PostSerializer(instance=post, context={'user':request.user}, many=False)
        posts = Post.objects.filter(topic=post.topic).exclude(uuid=id)
        related_posts_serializer = PostSerializer(instance=posts, context={'user':request.user}, many=True)
        return render(
            request,
            self.template_name,
            {
                'post': main_post_serializer.data,
                'posts': related_posts_serializer.data,
                'topic': post.topic,
                'user': request.user
            }
        )


class SearchView(View):
    template_name = 'app/search.html'

    def get(self, request):
        topics_max = CONSTANTS.get('TOPICS').get('MAX_SEARCH_SIZE')
        posts_max = CONSTANTS.get('POSTS').get('MAX_SEARCH_SIZE')
        term = request.GET.get('term')
        posts = get_search_posts_queryset(term)
        topics = get_search_topics_queryset(term)
        posts_next = (len(posts) > posts_max)
        topics_next = (len(topics) > topics_max)
        if (posts_next): posts = posts[0:(len(posts) - 1)]
        if (topics_next): topics = topics[0:(len(topics) - 1)]
        post_serializer = PostSerializer(instance=posts, context={'user':request.user}, many=True)
        topic_serializer = TopicSerializer(instance=topics, context={'user':request.user}, many=True)
        return render(
            request,
            self.template_name,
            {
                'topics': topic_serializer.data,
                'topics_next': topics_next,
                'topics_max': topics_max,
                'posts': post_serializer.data,
                'posts_next': posts_next,
                'posts_max': posts_max,
                'search_term': term,
                'user': request.user
            }
        )

    def post(self, request):
        term = request.POST.get('search_term')
        return redirect('/search?term=' + term)


class AccountView(View):
    template_name = 'app/account.html'

    def get(self, request, username):
        user_posts = Post.objects.filter(user__username=username, disabled_at__isnull=True)
        post_serializer = PostSerializer(instance=user_posts, context={'user':request.user}, many=True)
        user = User.objects.get(username=username, disabled_at__isnull=True)
        return render(
            request, 
            self.template_name, 
            { 
                'posts': post_serializer.data,
                'user': user,
                'account_page': True
            }
        )
