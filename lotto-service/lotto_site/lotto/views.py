# lotto_site/lotto/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import LottoTicket, LottoDraw, WinningResult
from .forms import LottoTicketForm
import random

@login_required
def purchase_ticket(request):
    if request.method == 'POST':
        form = LottoTicketForm(request.POST)
        if form.is_valid():
            ticket_type = form.cleaned_data['ticket_type']
            
            if ticket_type == 'AUTO':
                numbers = random.sample(range(1, 46), 6)
            else:
                numbers = sorted([int(n) for n in form.cleaned_data['numbers'].split(',')])
            
            # 현재 회차 계산 로직 필요
            current_round = LottoDraw.objects.count() + 1
            
            ticket = LottoTicket.objects.create(
                user=request.user,
                ticket_type=ticket_type,
                numbers=numbers,
                draw_round=current_round
            )
            
            messages.success(request, '로또 구매가 완료되었습니다.')
            return redirect('check_result')
    else:
        form = LottoTicketForm()
    
    return render(request, 'lotto/purchase.html', {'form': form})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def draw_winning_numbers(request):
    if request.method == 'POST':
        numbers = random.sample(range(1, 46), 7)
        winning_numbers = sorted(numbers[:6])
        bonus_number = numbers[6]
        
        draw = LottoDraw.objects.create(
            draw_round=LottoDraw.objects.count() + 1,
            winning_numbers=winning_numbers,
            bonus_number=bonus_number,
            draw_date=timezone.now()
        )
        
        # 당첨 결과 계산 로직
        calculate_winning_results(draw)
        
        messages.success(request, '당첨 번호가 추첨되었습니다.')
        return redirect('admin:index')
        
    return render(request, 'lotto/draw.html')

@login_required
def check_result(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-purchase_date')
    results = WinningResult.objects.filter(ticket__in=tickets)
    
    return render(request, 'lotto/check_result.html', {
        'results': results
    })

@user_passes_test(is_admin)
def statistics(request):
    total_tickets = LottoTicket.objects.count()
    total_winners = WinningResult.objects.exclude(rank__isnull=True).count()
    winners_by_rank = WinningResult.objects.exclude(rank__isnull=True).values('rank').annotate(count=Count('id'))
    
    return render(request, 'lotto/statistics.html', {
        'total_tickets': total_tickets,
        'total_winners': total_winners,
        'winners_by_rank': winners_by_rank
    })