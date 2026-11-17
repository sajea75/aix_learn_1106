from django.shortcuts import render
from .models import FishPrediction

def board_list(request):
    records = FishPrediction.objects.all().order_by('-created_at')
    return render(request, 'board/list.html', {'records': records})