from django.shortcuts import render, redirect
from .models import ContactMessage

def index(request):
    return render(request, 'main/index.html')

def fortune(request, sign):
    return render(request, f'main/{sign}.html')

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name    = request.POST.get('name'),
            email   = request.POST.get('email'),
            zodiac  = request.POST.get('zodiac'),
            message = request.POST.get('message'),
        )
        return redirect('/contact/?sent=true')

    sent = request.GET.get('sent')
    return render(request, 'main/contact.html', {'sent': sent})