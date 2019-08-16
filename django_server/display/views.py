""" These are the views that define what variables are passed to a page
    as well as what HTML templates each page uses.

    1. Home - directs to the home page of the website
    2. Firms - directs to the main firm table of the website
    3. Firm_Page - directs to the individual news pages of each firm
    4. SearchView - defines behavior when a search query is processed

"""


from django.shortcuts import render
from django.views.generic import ListView
from . import models


def home(request):

    return render(request, 'display/home.html', context={'title': 'Home'})


def firms(request):
    firms = models.Names.objects.all()

    return render(request, 'display/firms.html', context=dict(title='Firms', firms=firms))


def firm_page(request, **kwargs):
    assert kwargs['name']

    firm_name = kwargs['name']

    try:
        firm = models.Names.objects.filter(name=firm_name[:-1])[0]
    except IndexError:
        firm = firm_name

    news = firm.get_news()


    main_areas = firm.get_main_areas()

    if main_areas:
        main_areas = main_areas[0]

    if news == 'None':
        news = -1
    if main_areas == 'None':
        main_areas = -1

    return render(request, 'display/firm_generic.html',
                  context={'title': firm_name,
                           'firm': firm,
                           'news': news,
                           'main_areas': main_areas,
                           })


class SearchView(ListView):
    model = models.Names()
    template_name = 'display/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        model = models.Names()
        object_list = model.search_query(search_query=query)
        return object_list









