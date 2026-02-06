from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm

def about(request):
    return render(request, 'pages/about.html')

def policies(request):
    return render(request, 'pages/policies.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                # Send to admin (console in dev)
                send_mail(subject, message, from_email, ['admin@acholacakes.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('pages:success')
    return render(request, 'pages/contact.html', {'form': form})

def success_view(request):
    return render(request, 'pages/success.html')
