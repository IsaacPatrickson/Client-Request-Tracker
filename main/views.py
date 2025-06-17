from django.shortcuts import render

# Create your views here.
def dashboard(request):
    # your code here
    return render(request, 'main/dashboard.html')

def client_list(request):
    return render(request, 'main/client_list.html')