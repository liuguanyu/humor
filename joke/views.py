from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core import serializers
import time,json,re

from joke.models import Joke , JokeDelegate
from thirdpart import hao360fetcher , qiubaifetcher , jsonpatch , picbidclient , fetcher

# Create your views here.
def index(request):
    jokes = Joke.objects.order_by('-id')[0:15]

    return render(request, 'joke/index.html', {
        "jokes" : jokes
    })   

def get_joke_list(request , page_no) : 
    if page_no == "" :
        page_no = "2"

    page_no = int(page_no)
    
    if page_no < 2 :
        page_no = 2    

    per_page = 15 

    per_page = per_page + 1

    start = (page_no - 1) * per_page 
    end = start + per_page - 1 

    jokes = Joke.objects.order_by('-id')[start:end]

    data = serializers.serialize("json", jokes)        

    return HttpResponse(data)

def get_random(request) :
    jokes = Joke.objects.order_by('?')[0:1]

    data = serializers.serialize("json", jokes)
    return HttpResponse(data)

def detail(request, joke_id):
    joke = get_object_or_404(Joke, pk=joke_id)

    reg = re.compile("<img.*?src='(.*?)'.*?>", re.IGNORECASE | re.DOTALL | re.MULTILINE)

    def _deal_with_match (mch) :
        joke.image = mch.group(1)

        return '' 

    joke.content = reg.sub(_deal_with_match , joke.msg , 0)
    joke.content = re.sub(r'<.*?>' , ''  , joke.content)
    joke.content = re.sub(r'\\s+'  , ''  , joke.content).strip('\n')

    try :
        next = Joke.objects.filter(id__lt=joke_id).order_by('-id')[0]
    except :
        next = {}

    try :
        prev = Joke.objects.filter(id__gt=joke_id).order_by('id')[0]        
    except :
        prev = {}       

    return render(request, 'joke/detail.html', {
        'joke' : joke , 
        'prev' : prev ,
        'next' : next 
    }) 

def fetch_joke(request , user_id):   
    fch = fetcher.Fetcher()
    rets = fch.fetch(user_id)
        
    JokeDelegate.insertJokes(rets) 
    return HttpResponse("Fetching joke finished in " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))