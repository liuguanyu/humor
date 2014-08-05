from django.shortcuts import get_object_or_404, render

from joke.models import Joke

# Create your views here.
def index(request):
    pass;

def detail(request, joke_id):
    joke = get_object_or_404(Joke, pk=joke_id)
    return render(request, 'joke/detail.html', {'joke': joke})