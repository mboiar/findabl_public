
					<div class="col rating-cards">
						<ul>
						<li class="rating-card row">
							<div class="col-4" style="font-weight: 600;">Intensywność zapachów</div>
							<div class="col-3 input-discrete"> <a href="#decrease">-</a>{{ curr_val }}<a href="#increase">+</a></div>
						</li>
						<li class="rating-card row">
							<div class="col-4" style="font-weight: 600;">Natężenie światła</div>
							<div class="col-3 input-discrete"> <a href="#decrease">-</a>{{ curr_val }}<a href="#increase">+</a></div>
						</li>
						<li class="rating-card row">
							<div class="col-4" style="font-weight: 600;">Natężenie dźwięku</div>
							<div class="col-3 input-discrete"> <a href="#decrease">-</a>{{ curr_val }}<a href="#increase">+</a></div>
						</li>
						<li class="rating-card row">
							<div class="col-4" style="font-weight: 600;">Przestrzeń?</div>
							<div class="col-3 input-discrete"> <a href="#decrease">-</a>{{ curr_val }}<a href="#increase">+</a></div>
						</li>
					  </ul>
					</div>

 <div class="input-main">
        <input class="form-control mr-sm-2" type="search" placeholder="{% translate 'For example, type 'Trattoria'' %}"
            aria-label="Search" style="height: 3rem;border-radius: 2em 0 0 2em;max-width: 360px;" name="q">

 class PlaceSearchFormView(TemplateView):
     form_class = PlaceSearchForm
     template_name = 'places/search_form.html'

 class AdvancedSearchView(TemplateView):
     form_class = AdvancedSearchForm
     template_name = 'places/advanced_search_form.html'


 action="{% url 'places:search_results' %}"