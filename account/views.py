from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('store:product_list')
    else:
        user_form = UserCreationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
