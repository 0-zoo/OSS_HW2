from django import forms

class LottoTicketForm(forms.Form):
    TICKET_TYPE_CHOICES = [
        ('AUTO', '자동'),
        ('MANUAL', '수동'),
    ]
    
    ticket_type = forms.ChoiceField(choices=TICKET_TYPE_CHOICES, label='구매 방식')
    numbers = forms.CharField(required=False, label='번호 (수동선택시 콤마로 구분)')
    
    def clean_numbers(self):
        ticket_type = self.cleaned_data.get('ticket_type')
        numbers = self.cleaned_data.get('numbers')
        
        if ticket_type == 'MANUAL' and not numbers:
            raise forms.ValidationError('수동 선택 시 번호를 입력해주세요.')
            
        if ticket_type == 'MANUAL':
            try:
                numbers = [int(n.strip()) for n in numbers.split(',')]
                if len(numbers) != 6:
                    raise forms.ValidationError('6개의 번호를 입력해주세요.')
                if not all(1 <= n <= 45 for n in numbers):
                    raise forms.ValidationError('1부터 45 사이의 번호를 입력해주세요.')
                if len(set(numbers)) != 6:
                    raise forms.ValidationError('중복되지 않는 번호를 입력해주세요.')
            except ValueError:
                raise forms.ValidationError('올바른 형식으로 번호를 입력해주세요.')
        
        return numbers
