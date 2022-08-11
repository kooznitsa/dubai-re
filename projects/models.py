from django.db import models
from django.contrib.auth.models import User
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
    price_sqf = models.FloatField(blank=True, null=True)
    median_sqf = models.FloatField(blank=True, null=True)
    diff_percent = models.FloatField(blank=True, null=True)
    valuation = models.CharField(max_length=255, blank=True, null=True)

    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    featured_image = models.ImageField(null=True, blank=True, default='')
    created = models.DateTimeField(default=now, editable=False)

    @property
    def tags(self):
        tags_keys = ['views', 'discounted', 'cheap', 'distressed', 'investment', \
        'tenanted', 'vacant', 'metro', 'furnished', 'condition', 'luxury']
        tags_values = [self.views, self.discounted, \
            self.cheap, self.distressed, self.investment, self.tenanted, \
            self.vacant, self.metro, self.furnished, self.condition, self.luxury]
        tags_dict = dict(zip(tags_keys, tags_values))

        return [key for key in tags_dict if (tags_dict[key] == 1)]


    def __str__(self):
        return self.highlights

    class Meta:
        managed = False
        db_table = 'ready_flats'