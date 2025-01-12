# lotto_site/lotto/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class LottoTicket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('AUTO', '자동'),
        ('MANUAL', '수동'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=6, choices=TICKET_TYPE_CHOICES)
    numbers = models.JSONField()  # [1, 15, 21, 35, 38, 45] 형식으로 저장
    draw_round = models.IntegerField()
    
    def __str__(self):
        return f"Ticket {self.id} - Round {self.draw_round}"

class LottoDraw(models.Model):
    draw_round = models.IntegerField(unique=True)
    draw_date = models.DateTimeField()
    winning_numbers = models.JSONField()  # [1, 15, 21, 35, 38, 45] 형식으로 저장
    bonus_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(45)]
    )
    
    def __str__(self):
        return f"Draw Round {self.draw_round}"

class WinningResult(models.Model):
    ticket = models.OneToOneField(LottoTicket, on_delete=models.CASCADE)
    draw = models.ForeignKey(LottoDraw, on_delete=models.CASCADE)
    rank = models.IntegerField(null=True)  # 1-5등, null은 미당첨
    prize_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    
    def __str__(self):
        return f"Ticket {self.ticket.id} - Rank {self.rank}"