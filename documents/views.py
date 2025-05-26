# documents/views.py
from django.shortcuts import render
  
# documents/views.py (continued)
def conversion_view(request):
    return render(request, 'conversion/documento.html')  

# documents/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

# Login view in the documents app
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('conversion')  # Redirect to conversion page
        else:
            return render(request, 'login/index.html', {'error': 'Invalid email or password'})
    return render(request, 'login/index.html')

# Conversion view in the documents app
def conversion_view(request):
    return render(request, 'conversion/documento.html')
