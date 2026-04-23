from django.urls import path
from .views import social_home, view_post, create_post, create_comment, delete_post, delete_comment

urlpatterns = [
    path("", social_home, name="social_home"),
    path("post/<int:post_id>/", view_post, name="view_post"),
    path("post/create/", create_post, name="create_post"),
    path("post/<int:post_id>/comment/", create_comment, name="create_comment"),
    path("post/<int:post_id>/delete/", delete_post, name="delete_post"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
]