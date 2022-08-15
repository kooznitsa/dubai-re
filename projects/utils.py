from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg, Count, ExpressionWrapper, F, FloatField, Max, Min
from django.core import validators

from .models import Project


def paginate_projects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    
    return custom_range, projects


def get_stats():
    minimum_price = Project.objects.aggregate(minimum_price=Min('price'))['minimum_price']
    maximum_price = Project.objects.aggregate(maximum_price=Max('price'))['maximum_price']

    overall_avg_price = Project.objects.aggregate(average_price=Avg('price'))['average_price']
    overall_price_sqf = Project.objects.aggregate(average_sqf=Avg(ExpressionWrapper(F('price')/F('surface'), \
            output_field=FloatField())))['average_sqf']
    
    common_districts_list = Project.objects \
        .values('district') \
        .annotate(count=Count('district')) \
        .order_by('-count')[:3]
    most_common_districts = ', '.join([district['district'] for district in common_districts_list])

    common_nhoods_list = Project.objects \
        .values('neighborhood') \
        .annotate(count=Count('neighborhood')) \
        .order_by('-count')[:3]
    most_common_nhoods = ', '.join([nhood['neighborhood'] for nhood in common_nhoods_list])

    val_options = ['great value', 'good value', 'fair value', 'overvalued', 'highly overvalued']
    n_undervalued, n_overvalued = 0, 0
    for project in Project.objects.all():
        if project.valuation == 'great value' or project.valuation == 'good value':
            n_undervalued += 1
        elif project.valuation == 'overvalued' or project.valuation == 'highly overvalued':
            n_overvalued += 1

    return minimum_price, maximum_price, overall_avg_price, overall_price_sqf, \
        most_common_districts, most_common_nhoods, n_undervalued, n_overvalued, \
        val_options


def empty_query(query):
    if query in validators.EMPTY_VALUES:
        query = None
    elif query is not None and query.isnumeric():
        query = int(query)


def search_projects(request):
    keywords = request.GET.get('keywords', '')
    beds = request.GET.get('beds', None)
    baths = request.GET.get('baths', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    valuation = request.GET.get('valuation', '')

    empty_query(beds)
    empty_query(baths)

    minimum_price, maximum_price, overall_avg_price, overall_price_sqf, \
            most_common_districts, most_common_nhoods, n_undervalued, n_overvalued, \
            val_options = get_stats()

    if min_price == None or min_price == '':
        min_price = minimum_price
    if max_price == None or max_price == '':
        max_price = maximum_price

    keyword_queries = Q(highlights__icontains=keywords) | \
                    Q(amenities__icontains=keywords) | \
                    Q(building__icontains=keywords) | \
                    Q(district__icontains=keywords) | \
                    Q(neighborhood__icontains=keywords)

    projects = Project.objects.all().order_by('-created')
    projects = projects.distinct().filter(keyword_queries) if keywords else projects
    projects = projects.distinct().filter(beds__exact=beds) if beds else projects
    projects = projects.distinct().filter(baths__exact=baths) if baths else projects
    projects = projects.distinct().filter(Q(price__gte=min_price, price__lte=max_price) | \
        Q(price__isnull=True)).order_by('price') if min_price or max_price else projects

    objects_ids = [project.id for project in projects if ((project.valuation)==valuation)]
    projects = projects.distinct().filter(id__in=objects_ids) if valuation else projects

    return projects, keywords, beds, baths, min_price, max_price, valuation