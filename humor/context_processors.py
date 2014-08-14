from django.conf import settings
 
 
def global_settings(request):
    # return any necessary values
    return {
        'SITE_NAME' : u'\u54a9\u54c8\u54c8\u7b11\u8bdd\u7f51',
        'ROOT_URL'  : 'http://humors.sinaapp.com/',
        'DETAIL_URL' : 'detail/'
    }