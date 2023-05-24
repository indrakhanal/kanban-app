from django.db import models
from django.conf import settings


class KanBanBoard(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="board_user")
    board_member = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="board_member")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-id"]
        
    def __str__(self):
        return self.name
    
    @property
    def get_board_member_list(self):
        return list(self.board_member.values("id", "email"))


class Tags(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(KanBanBoard, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name


class Lane(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(KanBanBoard, on_delete=models.CASCADE, related_name="lane_board")
    display_order  = models.PositiveIntegerField(default=0, editable=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["display_order"]
        
    def __str__(self):
        return f"{self.board.name}-->{self.name}"
        
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Existing lane
            original_lane = Lane.objects.get(pk=self.pk)
            original_display_order = original_lane.display_order
            if original_display_order != self.display_order:
                lanes_in_board = Card.objects.filter(board=self.board).order_by("display_order")
                if self.display_order < original_display_order:
                    # Moving the lane towards the beginning of the board
                    for lane in lanes_in_board.filter(display_order__gte=self.display_order, display_order__lt=original_display_order):
                        lane.display_order += 1
                        lane.save()
                        
                else:
                    # Moving the lane towards the end of the board
                    for card in lanes_in_board.filter(display_order__gt=original_display_order, display_order__lte=self.display_order):
                        card.display_order -= 1
                        card.save()
        return super().save(*args, **kwargs)
        
    @property
    def get_board_detail(self):
        return list(KanBanBoard.objects.filter(id=self.board.id).values())


class Card(models.Model):
    title = models.CharField(max_length=50)
    description  = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    card_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name="card_lane")
    display_order = models.PositiveIntegerField(default=0, editable=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["display_order"]
        
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Existing card
            original_card = Card.objects.get(pk=self.pk)
            original_display_order = original_card.display_order
            if original_display_order != self.display_order:
                # Card's display_order has changed
                cards_in_lane = Card.objects.filter(lane=self.lane).order_by("display_order")
                if self.display_order < original_display_order:
                    # Moving the card towards the beginning of the lane
                    for card in cards_in_lane.filter(display_order__gte=self.display_order, display_order__lt=original_display_order):
                        card.display_order += 1
                        card.save()
                else:
                    # Moving the card towards the end of the lane
                    for card in cards_in_lane.filter(display_order__gt=original_display_order, display_order__lte=self.display_order):
                        card.display_order -= 1
                        card.save()
        super().save(*args, **kwargs)
    
    @property
    def get_card_user(self):
        return list(self.card_users.values("id", "email"))

    def __str__(self):
        return f"{self.lane.board.name} --> {self.title}"
    
    
class Comment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="card_comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="card_comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        