from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm
from .models import HoseAssociation, HoseContent


class IndexView(generic.ListView):
    template_name = 'hose_usage/index.html'
    context_object_name = 'latest_hoses_created'

    def get_queryset(self):
        return HoseAssociation.objects.order_by('-time_created')[:5]


class DetailView(generic.DetailView):
    model = HoseAssociation
    template_name = 'hose_usage/detail.html'


class ResultsView(generic.DetailView):
    model = HoseAssociation
    template_name = 'hose_usage/results.html'


def listen_content(request, hose_id):
    hose = get_object_or_404(HoseAssociation, pk=hose_id)
    try:
        selected_song = hose.hosecontent_set.get(pk=request.POST['choice'])
    except (KeyError, HoseContent.DoesNotExist):
        error_message = f"You didn't select a song"
        return render(request,
                      'hose_usage/detail.html',
                      {'hose': hose,
                       'error': error_message}
                      )
    else:
        selected_song.times_listened = F('times_listened') + 1
        selected_song.save()
        return HttpResponseRedirect(
            reverse('h:results', args=(hose_id,))
        )


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
