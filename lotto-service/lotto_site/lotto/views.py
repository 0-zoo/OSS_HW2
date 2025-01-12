# lotto_site/lotto/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import LottoTicket, LottoDraw, WinningResult
from .forms import LottoTicketForm
from django.db.models import Count
import random

def index(request):
    return render(request, 'lotto/index.html')

# def purchase_ticket(request):
#     if request.method == 'POST':
#         form = LottoTicketForm(request.POST)
#         if form.is_valid():
#             ticket_type = form.cleaned_data['ticket_type']
            
#             if ticket_type == 'AUTO':
#                 numbers = random.sample(range(1, 46), 6)
#             else:
#                 numbers = sorted([int(n) for n in form.cleaned_data['numbers'].split(',')])
            
#             current_round = LottoDraw.objects.count() + 1
            
#             # 비로그인 사용자를 위한 임시 저장
#             ticket = LottoTicket.objects.create(
#                 user=None,  # 비로그인 사용자는 user를 None으로 설정
#                 ticket_type=ticket_type,
#                 numbers=numbers,
#                 draw_round=current_round
#             )
            
#             messages.success(request, '로또 구매가 완료되었습니다.')
#             return redirect('lotto:purchase_result')
#     else:
#         form = LottoTicketForm()
    
#     return render(request, 'lotto/purchase.html', {'form': form})

def purchase_ticket(request):
    if request.method == 'POST':
        form = LottoTicketForm(request.POST)
        if form.is_valid():
            ticket_type = form.cleaned_data['ticket_type']

            # 번호 생성
            if ticket_type == 'AUTO':
                numbers = random.sample(range(1, 46), 6)
            else:
                numbers = sorted([int(n) for n in form.cleaned_data['numbers'].split(',')])

            current_round = LottoDraw.objects.count() + 1

            # user 필드 설정 (비로그인 상태에서는 None)
            user = request.user if request.user.is_authenticated else None

            # LottoTicket 객체 생성
            ticket = LottoTicket.objects.create(
                user=user,
                ticket_type=ticket_type,
                numbers=numbers,
                draw_round=current_round
            )

            messages.success(request, '로또 구매가 완료되었습니다.')
            return redirect('lotto:purchase_result')
    else:
        form = LottoTicketForm()

    return render(request, 'lotto/purchase.html', {'form': form})


def purchase_result(request):
    # 가장 최근 구매한 티켓 조회
    latest_ticket = LottoTicket.objects.order_by('-purchase_date').first()
    
    if not latest_ticket:
        messages.error(request, '구매한 로또가 없습니다.')
        return redirect('lotto:purchase_ticket')
    
    return render(request, 'lotto/purchase_result.html', {
        'ticket_type': latest_ticket.ticket_type,
        'numbers': latest_ticket.numbers
    })

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin, login_url='admin:login')
def draw_winning_numbers(request):
    winning_ticket = None

    if request.method == 'POST':
        sold_tickets = LottoTicket.objects.all()
        
        if sold_tickets:
            winning_ticket = random.choice(sold_tickets)
            
            draw_round = LottoDraw.objects.count() + 1
            draw = LottoDraw.objects.create(
                draw_round=draw_round,
                draw_date=timezone.now(),
                winning_numbers=winning_ticket.numbers,
                bonus_number=random.choice(range(1, 46))
            )
            
            winning_result = WinningResult.objects.create(
                ticket=winning_ticket,
                draw=draw,
                rank=1,
                prize_amount=1000000
            )
            
            messages.success(request, '당첨 번호가 추첨되었습니다.')

        return render(request, 'lotto/draw.html', {'winning_ticket': winning_ticket})

    return render(request, 'lotto/draw.html', {'winning_ticket': None})

def check_result(request):
    latest_draw = LottoDraw.objects.order_by('-draw_date').first()
    if latest_draw:
        winning_results = WinningResult.objects.filter(draw=latest_draw)
        context = {
            'draw': latest_draw,
            'results': winning_results
        }
    else:
        context = {
            'draw': None,
            'results': None
        }
    
    return render(request, 'lotto/check_result.html', context)

@user_passes_test(is_admin, login_url='admin:login')
def statistics(request):
    total_tickets = LottoTicket.objects.count()
    total_winners = WinningResult.objects.exclude(rank__isnull=True).count()
    winners_by_rank = WinningResult.objects.exclude(rank__isnull=True).values('rank').annotate(count=Count('id'))
    
    return render(request, 'lotto/statistics.html', {
        'total_tickets': total_tickets,
        'total_winners': total_winners,
        'winners_by_rank': winners_by_rank
    })