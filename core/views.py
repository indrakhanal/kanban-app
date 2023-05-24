from django.shortcuts import render
from .models import KanBanBoard, Tags, Lane, Card, Comment
from rest_framework import viewsets
from .serializers import (
    BoardSerializer, 
    TagSerializer,
    LaneSerializer,
    CardSerializers,
    CommentSerializer,)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from users.permission import IsAdminUser, IsBoardOwner
User = get_user_model()


class BoardView(viewsets.ModelViewSet):
    serializer_class =  BoardSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAdminUser, IsAuthenticated, IsBoardOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self, *args, **kwargs):
	    return KanBanBoard.objects.filter(board_member__id = self.request.user.id)
 
    def retrieve(self, request, *args, **kwargs):
        board = KanBanBoard.objects.get(id = kwargs.get("pk"))
        board_serializer=BoardSerializer(board)
        board_serializer_data=board_serializer.data.copy()
        board_serializer_data['board_members']=board.get_board_member_list
        # board_data = {}
        # board_data["id"] = board.id
        # board_data["name"] = board.name
        # board_data["user_id"] = board.user.id
        # board_data["board_member"] = board.get_board_member_list
        # board_data["created_at"] = board.created_at
        lane = Lane.objects.filter(board__id = kwargs.get("pk")).values()
        cards = Card.objects.filter(lane__board__id = kwargs.get("pk")).values()
        tags = Tags.objects.filter(board__id = kwargs.get("pk")).values()
        
        board_serializer_data["lane"]=list(lane)
        board_serializer_data["cards"]=list(cards)
        board_serializer_data["tags"]=list(tags)
        return Response(board_serializer_data)
        
 
class InviteMember(APIView):
    """
    API for invite a new member to the individual board.
    
    request parameter is look like:  
    
        {BASE_URL}/member/invite/{board_id}/?email=example@example.com
        
        OR email can be send from form data.
    """
    permission_classes = (IsAuthenticated, IsBoardOwner,)

    def post(self, request, *args, **kwargs):
       
        email = self.request.POST.get("email", None)
        if email is not None:
            users = User.objects.filter(email=email)
            if users:
                board_id = kwargs.get("pk")
                board_obj = KanBanBoard.objects.get(id=board_id)
                board_obj.board_member.add(*users)
                return Response(data = "User Invited Successfully", status=status.HTTP_200_OK)
            else:
                return Response(data="No users found with the provided email.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="Invite Failed", status=status.HTTP_400_BAD_REQUEST)

        
class RemoveMember(APIView):
    """
    API for remove member from the board.
    
    request parameter is look like:  
    
        {BASE_URL}/member/remove/{board_id}/?email=example@example.com
        
        OR email can be send from form data.
    """
    permission_classes = (IsAuthenticated, IsAdminUser, IsBoardOwner)

    def post(self, request, *args, **kwargs):
        email = self.request.POST.get("email", None)
        if email is not None:
            users = User.objects.filter(email=email)
            if users:
                board_id = kwargs.get("pk")
                board_obj = KanBanBoard.objects.get(id=board_id)
                board_obj.board_member.remove(*users)
                return Response(data=f"{email} member removed", status=status.HTTP_200_OK)
            else:
                return Response(data=f"No users found with {email}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="Please Provide an email.", status=status.HTTP_400_BAD_REQUEST)
            
            
class SearchUser(APIView):
    """
    API for search an User from their username or email
    
    request parameter is look like:
    
        {BASE_URL}/member/search/?email=example@example.com
        
        OR 
        
        {BASE_URL}/member/search/?email=example
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_email = self.request.GET.get("email", None)
        if user_email is not None:
            user_detail = User.objects.filter(
                Q(email__icontains=user_email)
                | Q(username__icontains=user_email.split('@')[0])
                ).values("id", "email")
            return Response(list(user_detail))
        else:
            return Response([])
 
    
class TagView(viewsets.ModelViewSet):
    serializer_class =  TagSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    
    def get_queryset(self, *args, **kwargs):
	    return Tags.objects.filter(board__board_member__id = self.request.user.id)
    
    
class LaneView(viewsets.ModelViewSet):
    serializer_class =  LaneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'display_order']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAdminUser, IsAuthenticated, IsBoardOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self, *args, **kwargs):
	    return Lane.objects.filter(board__board_member__id = self.request.user.id)
 
    def retrieve(self, request, *args, **kwargs):
        lane = get_object_or_404(Lane, id=kwargs.get("pk"))
        lane_serializer = LaneSerializer(lane)
        lane_serializer_data = lane_serializer.data.copy()
        lane_serializer_data["board_detail"] = lane.get_board_detail
        
        cards = Card.objects.filter(lane__id=kwargs.get("pk")).values()
        lane_serializer_data["cards"] = list(cards)
        return Response(lane_serializer_data)
 
 
class CardView(viewsets.ModelViewSet):
    """
    Only Authenticated user can access this View.
    
    **
    """
    serializer_class =  CardSerializers
    queryset = Card.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['display_order']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAdminUser, IsAuthenticated, IsBoardOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(lane__board__board_member__id = self.request.user.id)
 
    def retrieve(self, request, *args, **kwargs):
        card = get_object_or_404(Card, id=kwargs.get("pk"))
        card_detail = {}
        card_detail["id"] = card.id
        card_detail["title"] = card.title
        card_detail["description"] = card.description
        card_detail["lane"] = card.lane.id
        card_detail["display_order"] = card.display_order
        card_detail["card_members"] = card.get_card_user
        card_detail["created_at"] = card.created_at
        
        comment = Comment.objects.filter(card__id=kwargs.get("pk")).values()
        data = {}
        data["card"] = card_detail
        data["comment"] = list(comment)
        return Response(data)
        

class CommentView(viewsets.ModelViewSet):
    serializer_class =  CommentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    
    def get_queryset(self, *args, **kwargs):
	    return Comment.objects.filter(card__lane__board__user__id = self.request.user.id)
