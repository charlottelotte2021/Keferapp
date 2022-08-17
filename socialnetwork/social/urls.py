from asyncio import as_completed
from django.urls import path 
from .views import PostDeleteView, PostListView, PostDetailView, PostEditView, ProfileView, ProfileEditView, Search, CreateThread, ListThreads, ThreadView, CreateMessage, ThreadNotification, RemoveNotification
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    # path('explore/', ExplorePage.as_view(), name='explore'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name= 'post-delete'),
    path('profile/<int:pk>', ProfileView.as_view(), name= 'profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name= 'profile-edit'),
    path('search/', Search.as_view(), name='search'),
    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/',CreateMessage.as_view(), name='create-message'),
    # path('notification/<int:notification_pk>/post/<int:post_pk>/', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
    # path('inbox/thread/', WriteUser.as_view(), name='thread'),
]

