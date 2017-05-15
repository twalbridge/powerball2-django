from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin, ListView

from .forms import EntryForm
from .models import Entry, PopularSelection


class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
    	if not hasattr(self, 'ajax_template_name'):
    		split = self.template_name.split('.html')
    		split[-1] = '_inner'
    		split.append('.html')
    		self.ajax_template_name = ''.join(split)
    		if request.is_ajax():
    			self.template_name = self.ajax_template_name
    		return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class EntryListView(AjaxTemplateMixin, ListView):
    model = Entry
    template_name = 'playball/all_results.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
    	"""Handles context to the template_name."""
    	context = super(EntryListView, self).get_context_data(**kwargs)
    	popular_selection = get_object_or_404(PopularSelection, pk=1)
    	context['current_most_popular'] = popular_selection.current_most_popular
    	return context


class PopularEntryView(AjaxTemplateMixin, ListView):
    model = PopularSelection
    template_name = 'playball/result.html'

    def get_context_data(self, **kwargs):
        """Handles context to the template_name."""
        context = super(PopularEntryView, self).get_context_data(**kwargs)
        popular_selection = get_object_or_404(PopularSelection, pk=1)
        context['current_most_popular'] = popular_selection.current_most_popular
        return context


class EntryCreateView(SuccessMessageMixin, AjaxTemplateMixin, CreateView):
    model = Entry
    template_name = 'homepage.html'
    form_class = EntryForm
    success_url = reverse_lazy('home')
    success_message = (
    	"%(one)s - %(two)s - %(three)s - %(four)s - %(five)s and PowerBall \
    	%(power)s have been successfully entered for %(enteree)s"
    )

    def get_context_data(self, **kwargs):
    	"""Handles context to the template_name."""
    	context = super(EntryCreateView, self).get_context_data(**kwargs)
    	popular_selection = get_object_or_404(PopularSelection, pk=1)
    	context['current_most_popular'] = popular_selection.current_most_popular
    	context['title'] = "New Entry"
    	context['body'] = "Fill in this form with your first and last name, \
    		your choice of five favorite numbers within the range of 1 through \
    		69 (no duplicates) and your powerball number pick within the range \
    		of 1 through 26."
    	context['entry_list'] = Entry.objects.all()
    	return context

    def get_success_message(self, cleaned_data):
    	"""Handles the sucess message."""
    	return self.success_message % dict(
    		cleaned_data,
    		one=self.object.first_favorite,
    		two=self.object.second_favorite,
    		three=self.object.third_favorite,
    		four=self.object.fourth_favorite,
    		five=self.object.fifth_favorite,
    		power=self.object.power_ball_number,
    		enteree=self.object.first_name,
    	)

