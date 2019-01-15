from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import HoseUser, HoseAssociation, HoseContent


class IndexView(generic.ListView):
    template_name = 'hose_usage/index.html'
    context_object_name = 'hoses_shared'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            username = self.request.user.username
        h_associations = HoseAssociation.objects.order_by('-time_created')
        for ha in h_associations:
            other_name = ha.get_other_end(username)
            setattr(ha, 'other_name', ha)
        return h_associations


class FindUsersView(generic.ListView):
    model = HoseUser
    template_name = 'hose_usage/show_users.html'


def find_listen(request):
    max_associations = 10
    max_songs = 50
    template_name = 'hose_usage/find_listen.html'
    context_object_name = 'music_suggestion'

    current_user = request.user
    h_associations = HoseAssociation.objects\
        .filter(Q(first_end=current_user) | Q(second_end=current_user))\
        .order_by('?')[:max_associations]
    if h_associations.count() == 0:
        raise ValueError(f"This user {current_user.username} has no available hose")
    h_songs = HoseContent.objects.filter(hose_from__id__in=h_associations.values('id')).all()[:max_songs]
    if h_songs.count() == 0:
        raise ValueError(f"This user {current_user.username} has no available songs")
    return render(request,
                  template_name,
                  {context_object_name: h_songs}
                  )


class ShowUsers(generic.ListView):
    model = HoseUser
    template_name = 'hose_usage/show_users.html'
    context_object_name = 'user_hosers'

    def get_queryset(self):
        current_user = self.request.user
        h_associations = HoseAssociation.objects\
            .filter(Q(first_end=current_user) | Q(second_end=current_user)).all()
        other_names = []
        for association in h_associations:
            other_name = association.get_other_end(current_user.username)
            other_names.append(other_name)
        hosers = HoseUser.objects.filter(username__in=other_names).all()
        return hosers






class DetailView(generic.DetailView):
    model = HoseContent
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
