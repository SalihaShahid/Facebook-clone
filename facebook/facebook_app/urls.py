from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns=[
path("signup",signup,name="signup"),#done
path("authenticate<str:email>",authenticate,name="authenticate"),#done
path("login",login,name="login"),#done
path("",home,name="home"),
path("search",search,name="search"),#done
path("add_friend<str:email>",add_friend,name='add_friend'),
path("view_requests",view_requests,name="view_requests"),
path("accept_request<str:email>",accept_request,name="accept_request"),
path("logout",logout,name="logout"),
path("reject_request<str:email>",reject_request,name="reject_request"),
path("view_friends",view_friends,name="view_friends"),
path("view_profile<str:email>",view_profile,name="view_profile"),
path("chat<str:email>",chat,name="chat"),
path("text_post",text_post,name="text_post"),
path("media_post",media_post,name="media_post"),
path("your_posts",your_posts,name="your_posts"),
path("text_post_like<int:id>",text_post_like,name="text_post_like"),
path("media_post_like<int:id>",media_post_like,name="media_post_like"),
path("text_post_comment<int:id>",text_post_comment,name="text_post_comment"),
path("media_post_comment<int:id>",media_post_comment,name="media_post_comment"),
path("view_text_comments<int:id>",view_text_comments,name="view_text_comments"),
path("view_media_comments<int:id>",view_media_comments,name="view_media_comments"),
path("view_text_likes<int:id>",view_text_likes,name="view_text_likes"),
path("view_media_likes<int:id>",view_media_likes,name="view_media_likes"),
path("view_user_profile<str:email>",view_user_profile,name="view_user_profile"),
path("update_profile",update_profile,name="update_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)