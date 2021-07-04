from interactions.topic.api.list_topics import ListTrendingTopics, SearchTopics
from interactions.post.api.cud_posts import CreatePost, DeletePost
from interactions.post.api.list_posts import ListPosts
from interactions.likes.cud_likes import CreateCommentDislike, CreateCommentLike, CreatePostDislike, CreatePostLike, DeleteCommentDislike, DeleteCommentLike, DeletePostDislike, DeletePostLike
from django.urls import re_path
from interactions.comment.api.cud_comments import CreatePostComment, DeletePostComment
from interactions.comment.api.list_comments import ListPostComments

urlpatterns = [
    # Comment crud.
    re_path(r'^comments/create', CreatePostComment.as_view()),
    re_path(r'^comments/delete', DeletePostComment.as_view()),
    re_path(r'^comments/list', ListPostComments.as_view()),
    # Comment likes.
    re_path(r'^comments/like', CreateCommentLike.as_view()),
    re_path(r'^comments/unlike', DeleteCommentLike.as_view()),
    re_path(r'^comments/dislike', CreateCommentDislike.as_view()),
    re_path(r'^comments/undislike', DeleteCommentDislike.as_view()),
    # Post crud.
    re_path(r'^posts/create', CreatePost.as_view()),
    re_path(r'^posts/delete', DeletePost.as_view()),
    re_path(r'^posts/list', ListPosts.as_view()),
    # Post likes.
    re_path(r'^posts/like', CreatePostLike.as_view()),
    re_path(r'^posts/unlike', DeletePostLike.as_view()),
    re_path(r'^posts/dislike', CreatePostDislike.as_view()),
    re_path(r'^posts/undislike', DeletePostDislike.as_view()),
    # Topics crud.
    re_path(r'^topics/trending', ListTrendingTopics.as_view()),
    re_path(r'^topics/search', SearchTopics.as_view()),
]
