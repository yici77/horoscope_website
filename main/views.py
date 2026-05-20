import os
from django.shortcuts import render, redirect
from django.conf import settings
from .models import ContactMessage

def index(request):
    return render(request, 'main/index.html')

def fortune(request, sign):
    # Read mood quote from txt file
    quote_path = os.path.join(settings.BASE_DIR, 'scraper', 'quotes', f'{sign}_quote.txt')
    try:
        with open(quote_path, 'r', encoding='utf-8') as f:
            quote = f.read().strip()
    except FileNotFoundError:
        quote = ''

    return render(request, f'main/{sign}.html', {'quote': quote})

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

def imprint(request):
    return render(request, 'main/imprint.html')

def about(request):
    return render(request, 'main/about.html')