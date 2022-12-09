from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import F, Avg
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit

from .models import Place, Review, MIN_SCORE, MAX_SCORE
from .forms import AdvancedSearchForm1, AdvancedSearchForm2, AdvancedSearchForm3, ReviewForm

NAME_DICTS = {
        ('location', 'Location'): dict(Place.LOCATION_CHOICES),
        ('type', 'Type'): dict(Place.TYPE_CHOICES),
        ('access', 'Accessibility'): dict(Review.SCORE_CATEGORY_CHOICES)
    }

class PlaceDetailView(DetailView):
    """Displays the details about an instance of the `place` model"""

    model = Place
    template_name = 'places/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['max_score'] = MAX_SCORE
        context['min_score'] = MIN_SCORE
        review_count = self.object.review_set.count()
        context['review_count'] = review_count
        review_scores = self.object.get_review_scores()
        if review_count:
            context['scores'] = [{
                'circle_scale': Review.get_score_circle_scale(sc),
                'name': name[0],
                'verbose_name': name[1],
                'value': sc,
                'score_color': Review.get_score_color_value(sc)
                } for (name,sc) in zip(Review.SCORE_CATEGORY_CHOICES + [('score_avg', _('Average'))], review_scores + [sum(review_scores) / len(review_scores)])]    # get scores' context
        if self.request.user.is_authenticated:
            context['review'] = Review.objects.safe_get(user=self.request.user, place=self.object)    # get current user's review
        return context

class SearchResultsView(ListView):
    """Displays search results"""

    model = Place
    filter_options = NAME_DICTS.keys()
    template_name = 'places/search_results.html'
    paginate_by = 5

    def get_queryset(self):
        if not self.request.session.get('filter-results'):
            self.q = dict(self.request.GET.lists())
        else:
            self.request.session['filter-results'] = False
            self.q = self.request.session.get('q', {})
        main_score_name = self.q.get('access', [None])[0]
        if main_score_name:
            main_score = Avg('review__' + main_score_name)
        else:
            main_score = sum(Avg('review__'+score_name[0]) for score_name in Review.SCORE_CATEGORY_CHOICES) / len(Review.SCORE_CATEGORY_CHOICES)
        place_list = Place.objects.annotate(score=main_score).search(self.q)
        return place_list.annotate(
            score_circle_scale=Review.get_score_circle_scale(F('score')),
            score_color=Review.get_score_color_value(F('score'))
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name_dicts"] = NAME_DICTS
        context["filters"] = self.filter_options
        context["queries"] = self.q if self.q else dict(self.request.GET.lists())
        return context

    def __init__(self, q=None, **kwargs) -> None:
        self.q = q
        super().__init__(**kwargs)

def filter_search(request):
    """Displays filter form"""

    forms = [
        (AdvancedSearchForm1, {'location' : request.session.get('location', None)}),
        (AdvancedSearchForm2, {'type' : request.session.get('type', None)}),
        (AdvancedSearchForm3, {'access' : request.session.get('access', None)})

    ]
    request.session['filter-results'] = False
    steps = len(forms)
    step = int(request.GET.get('goto_step', int(request.GET.get('step', 0))+1))
    template = 'places/generic_search_form.html'
    queries =  {key: list(set(vals)) for key, vals in request.GET.lists() if key in (key[0] for key in NAME_DICTS.keys())}
    # request.session['q'] = {}
    if not request.session.get('q', None): request.session['q'] = {}
    request.session['q'].update(queries)
    if step-1==steps:
        request.session['filter-results'] = True
        return SearchResultsView.as_view()(request, q=request.session['q'])
    context = {
        'form': forms[step-1][0](initial=forms[step-1][1], auto_id=False),
        'step': step,
        # 'queries': queries,
        'steps': {
            'step':step, 
            'count':steps, 
            'prev': max(step-1, 0)
            }
        }
    return render(request, template, context)

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = 'about.html'

@method_decorator(ratelimit(key='ip', rate='10/m', method='POST'), name='post')
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'places/review_create_form.html'
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.place = get_object_or_404(Place, id=self.kwargs['pk'])
        r = super().form_valid(form)
        return r

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = {'place':get_object_or_404(Place, id=self.kwargs['pk'])}
        return context

    def get_success_url(self):
        return (reverse_lazy('places:place', args=(self.kwargs['pk'],)))

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """deletes a ``Review`` instance."""

    model = Review
    template_name = 'places/review_confirm_delete.html'

    def get_object(self):
        return Review.objects.get(user=self.request.user, place=get_object_or_404(Place, id=self.kwargs['pk']))

    def get_success_url(self):
        return (reverse_lazy('places:place', args=(self.kwargs['pk'],)))
        
class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """updates a ``Review`` instance."""

    model = Review
    template_name = 'places/review_create_form.html'
    form_class = ReviewForm

    def get_object(self, queryset):
        return Review.objects.get(user=self.request.user, place=get_object_or_404(Place, id=self.kwargs['pk']))

    def get_success_url(self):
        return (reverse_lazy('places:place', args=(self.kwargs['pk'],)))
