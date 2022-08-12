from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, ExpressionWrapper, F, FloatField
from django.utils.timezone import now
import uuid


class Project(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    listing_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    building = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    beds = models.FloatField(blank=True, null=True)
    baths = models.IntegerField(blank=True, null=True)
    surface = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    highlights = models.TextField(max_length=100, blank=True, null=True)
    furnishing = models.CharField(max_length=255, blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    featured_image = models.ImageField(null=True, blank=True, default='')
    created = models.DateTimeField(default=now, editable=False)
    completion_year = models.CharField(max_length=4, blank=True, null=True)
    floor = models.CharField(max_length=3, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True, default=0)
    discounted = models.IntegerField(blank=True, null=True, default=0)
    cheap = models.IntegerField(blank=True, null=True, default=0)
    distressed = models.IntegerField(blank=True, null=True, default=0)
    investment = models.IntegerField(blank=True, null=True, default=0)
    tenanted = models.IntegerField(blank=True, null=True, default=0)
    vacant = models.IntegerField(blank=True, null=True, default=0)
    metro = models.IntegerField(blank=True, null=True, default=0)
    furnished = models.IntegerField(blank=True, null=True, default=0)
    condition = models.IntegerField(blank=True, null=True, default=0)
    upgraded = models.CharField(max_length=255, blank=True, null=True)
    luxury = models.IntegerField(blank=True, null=True, default=0)

    @property
    def tags(self):
        tags_keys = ['views', 'discounted', 'cheap', 'distressed', 'investment', \
        'tenanted', 'vacant', 'metro', 'furnished', 'condition', 'luxury']
        tags_values = [self.views, self.discounted, \
            self.cheap, self.distressed, self.investment, self.tenanted, \
            self.vacant, self.metro, self.furnished, self.condition, self.luxury]
        tags_dict = dict(zip(tags_keys, tags_values))

        return [key for key in tags_dict if (tags_dict[key] == 1)]

    @property
    def sqf_price(self):
        return self.price / self.surface

    @property
    def avg_price_sqf(self):
        if self.price and self.surface:
            return agg_price(self, prices_avg_sqf, 'avg_sqf')
        else:
            return ''

    @property
    def avg_price(self):
        if self.price and self.surface:
            return agg_price(self, prices_avg, 'avg')
        else:
            return ''

    @property
    def price_diff(self):
        if self.price and self.surface:
            return self.sqf_price / self.avg_price_sqf * 100 - 100
        else:
            return ''

    @property
    def valuation(self):
        if self.price and self.surface:
            return val_conditions(self.price_diff)
        else:
            return ''

    def __str__(self):
        return self.highlights

    class Meta:
        managed = False
        db_table = 'dubai_flats'



def val_conditions(price_diff):
    if (price_diff <= -50):
        return 'great value'
    elif (price_diff > -50) & (price_diff <= -30):
        return 'good value'
    elif (price_diff > -30) & (price_diff <= 30):
        return 'fair value'
    elif (price_diff > 30) & (price_diff <= 50):
        return 'overvalued'
    elif (price_diff > 50):
        return 'highly overvalued'


def overall_average():
    prices_avg_sqf = Project.objects.values('district', 'beds', 'baths') \
        .distinct() \
        .annotate(avg_sqf=Avg(ExpressionWrapper(F('price')/F('surface'), output_field=FloatField()))) \
        .order_by()

    prices_avg = Project.objects.values('district', 'beds', 'baths') \
        .distinct() \
        .annotate(avg=Avg(ExpressionWrapper(F('price'), output_field=FloatField()))) \
        .order_by()

    return prices_avg_sqf, prices_avg

prices_avg_sqf, prices_avg = overall_average()


def agg_price(project, price_list, new_var):
    for i in price_list:
        if project.district == i['district'] and \
            project.beds == i['beds'] and \
            project.baths == i['baths']:
                return i[new_var]
