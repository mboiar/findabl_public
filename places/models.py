from random import choice

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import UniqueConstraint, QuerySet, Avg
from django.http import QueryDict
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

DEFAULT_ORDER = 'score_avg'
MIN_SCORE = 1
MAX_SCORE = 5
CIRCLE_SCALE = 251
ScoreValidators = [MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)]

class PlaceQuerySet(QuerySet):

    def search(self, query_dict: QueryDict):
        qs = self
        q = query_dict.get('q', [None])
        q = q[0] # TODO: Full search
        if q:
            qs = qs.filter(name__icontains=q)
        qtypes = query_dict.get('type')
        if qtypes:
            qs = qs.filter(type__in=qtypes)

        qlocations = query_dict.get('location')
        if qlocations:
            qs = qs.filter(location__in=qlocations)
        
        qsort_option = query_dict.get('access', [None])[0]
        if qsort_option:
            qs = qs.order_by('score')
        return qs

class ReviewManager(models.Manager):

    def safe_get(self, user, place):
        """Custom `get` method for a `Review` model
        
        Like `get` method of a `Review` model, but returns `None` instead of raising a `DoesNotExist` error, when there are no matches in the database lookup"""

        qs = self
        try:
            qs = qs.get(user=user, place=place)
        except self.model.DoesNotExist:
            qs = None
        return qs


class Place(models.Model):

    ETH = "ETH"
    FAS = "FAS"
    # CAS = "CAS"
    FAM = "FAM"
    RES = "RES"
    CAF = "CAF"
    BAR = "BAR"
    OTH = "OTH"
    PIZ = "PIZ"

    TYPE_CHOICES = [
        (ETH, _('Ethnic')),
        (BAR, _('Bar')),
        (PIZ, _('Pizzeria')),
        (CAF, _('Café')),
        (FAS, _('Fast food')),
        (RES, _('Restaurant')),
        (FAM, _('Family-friendly')),
        (OTH, _('Other'))
    ]

    MOK = 'MOK'
    PPE = 'PRE'
    URW = 'URW'
    WOL = 'WOL'
    BIE = 'BIE'
    TAR = 'TAR'
    SRO = 'SRO'
    BEM = 'BEM'
    BIA = 'BIA'
    OCH = 'OCH'
    WAW = 'WAW'
    PPC = 'PPC'
    URS = 'URS'
    ZOL = 'ZOL'
    WLO = 'WLO'
    WIL = 'WIL'
    REM = 'REM'
    WES = 'WES'

    LOCATION_CHOICES = [
        (MOK, _('MOKOTÓW')),
        (PPE, _('PRAGA-POŁUDNIE')),
        (URW, _('URSYNÓW')),
        (WOL, _('WOLA')),
        (BIE, _('BIELANY')),
        (TAR, _('TARGÓWEK')),
        (SRO, _('ŚRÓDMIEŚCIE')),
        (BEM, _('BEMOWO')),
        (BIA, _('BIAŁOŁĘKA')),
        (OCH, _('OCHOTA')),
        (WAW, _('WAWER')),
        (PPC, _('PRAGA-PÓŁNOC')),
        (URS, _('URSYNÓW')),
        (ZOL, _('ŻOLIBORZ')),
        (WLO, _('WŁOCHY')),
        (WIL, _('WILANÓW')),
        (REM, _('REMBERTÓW')),
        (WES, _('WESOŁA'))
    ]

    name = models.CharField(_("Name"), max_length=240)
    location = models.CharField(_("Location"), max_length=4, choices=LOCATION_CHOICES)
    address = models.CharField(_("Address"), max_length=240)
    url =  models.URLField(_("Url on Google Maps"), unique=True)
    type = models.CharField(_("Type"), choices=TYPE_CHOICES, max_length=30, default=("OTH", _("Other")))
    objects = PlaceQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('places:place', kwargs={'pk': self.pk})

    def get_score(self, score_name: str) -> int:
        if not self.review_set.count():
            return None
        return self.review_set.aggregate(Avg(score_name))[score_name+'__avg']

    def get_review_scores(self):
        if not self.review_set.count():
            return []
        else:
            return [self.get_score(score_name[0]) for score_name in Review.SCORE_CATEGORY_CHOICES]

    def __str__(self):
        return self.name

class Review(models.Model):
    """ Represents a user review """
    SCORE_CATEGORY_CHOICES = [
        ('sin', _("Sensory intensity")),
        ('wac', _("Wheelchair accessibility")),
        ('noi', _("Quiet")),
        ('lsi', _("Low-sight friendliness"))
    ]
    SCORE_CHOICES = [(i,i) for i in range(MIN_SCORE, MAX_SCORE)]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name=_("Place"), on_delete=models.CASCADE)
    creation_date = models.DateTimeField(_("Creation date"), auto_now_add=True)
    # score_avg = models.FloatField(_("Average rating"), default=0)
    sin = models.IntegerField(_("Sensory intensity"), choices=SCORE_CHOICES, blank=False, default=1, validators=ScoreValidators)
    wac = models.IntegerField(_("Wheelchair accessibility"), choices=SCORE_CHOICES, blank=False, default=1, validators=ScoreValidators)
    noi = models.IntegerField(_("Noise"), choices=SCORE_CHOICES, blank=False, default=1, validators=ScoreValidators)
    lsi = models.IntegerField(_("Low-sight friendly"), choices=SCORE_CHOICES, blank=False, default=1, validators=ScoreValidators)
    objects = ReviewManager()

    def get_score_circle_scale(score):
        return (1 - score / (MAX_SCORE)) * CIRCLE_SCALE
    
    def get_score_color_value(score):
        return 255 - score * 255 / MAX_SCORE
        
    
    class Meta:
       constraints = [
			UniqueConstraint(fields=['user', 'place'], name=_('One review per place'))
		]

    def __str__(self):
        return "{0}: {1}".format(self.user.id, self.place.name)

# class City