from django.urls import path, include
from rest_framework import routers
from .views import (BoardView,
                    TagView, 
                    LaneView,
                    CardView, 
                    CommentView, 
                    InviteMember, 
                    RemoveMember, 
                    SearchUser, )
app_name = 'core'
router = routers.DefaultRouter()
router.register('board', BoardView, 'board')
router.register('tags', TagView, 'tags')
router.register('lane', LaneView, 'lane')
router.register('card', CardView, 'card')
router.register('comment', CommentView, 'comment')




urlpatterns = [
    path('api/', include(router.urls)),
    path('api/member/invite/<int:pk>/', InviteMember.as_view(), name="invite-member"),
    path('api/member/remove/<int:pk>/', RemoveMember.as_view(), name="remove-member"),
    path('api/member/search/', SearchUser.as_view(), name="search-member"),
    # 
    
]