from django.shortcuts import get_object_or_404, render

def home(request):
    context = {}
    return render(request, 'home/index.html', context)    