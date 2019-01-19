from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import HoseUser, HoseAssociation, HoseContent

# class HoseUsageLoginRequiredMixin(LoginRequiredMixin):
#     """Custom mixin for login required"""
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'


class HomeView(generic.ListView):
    """Home view of user"""
    template_name = 'hose_usage/index.html'
    context_object_name = 'hoses_shared'

    def get_queryset(self):
        user_id = self.request.user.id
        h_associations = HoseAssociation.objects. \
            filter(Q(first_end__id=user_id) | Q(second_end__id=user_id)). \
            order_by('-time_last_update').all()
        results = []
        for ha in h_associations:
            ha_dict = ha.as_dict()
            if ha_dict['first_end_id'] == user_id:
                ha_dict['other_user_id'] = ha_dict['second_end_id']
                ha_dict['other_user_username'] = ha_dict['second_end_username']
            else:
                ha_dict['other_user_id'] = ha_dict['first_end_id']
                ha_dict['other_user_username'] = ha_dict['first_end_username']
            results.append(ha_dict)
        return results


class LinkedHosesView(generic.ListView):
    """User view to see their linked hoses"""
    template_name = 'hose_usage/hoses.html'
    context_object_name = 'hoses_shared'

    def get_queryset(self):
        user_id = self.request.user.id
        h_associations = HoseAssociation.objects. \
            filter(Q(first_end__id=user_id) | Q(second_end__id=user_id)). \
            order_by('-time_created').all()
        results = []
        for ha in h_associations:
            nb_songs = HoseContent.objects.filter(hose_from__id=ha.id).count()
            ha_dict = ha.as_dict()
            if ha_dict['first_end_id'] == user_id:
                ha_dict['other_user_id'] = ha_dict['second_end_id']
                ha_dict['other_user_username'] = ha_dict['second_end_username']
            else:
                ha_dict['other_user_id'] = ha_dict['first_end_id']
                ha_dict['other_user_username'] = ha_dict['first_end_username']
            ha_dict['nb_songs'] = nb_songs
            results.append(ha_dict)
        return results


def browser_hosers(request):
    """Render a portion of HoseUser"""
    user_id = request.user.id
    max_hosers = 20
    hus = HoseUser.objects.filter(~Q(id=user_id))[:max_hosers]
    for hu in hus:
        other_id = hu.id
        ha = HoseAssociation.objects.filter(
            (Q(first_end=user_id) and Q(second_end=other_id))
            or
            (Q(first_end=other_id) and Q(second_end=user_id))
        )
        if len(ha) > 0:
            setattr(hu, 'has_hose', True)
            setattr(hu, 'hose_id', ha[0].id)
        else:
            setattr(hu, 'has_hose', False)
            setattr(hu, 'hose_id', -1)
    return render(request, 'hose_usage/browse_hosers.html', {
        'hose_users': hus,
    })


def show_hoser(request, hoser_id):
    """Render minimal info about a user"""
    template_name = 'hose_usage/show_hoser.html'
    user_id = request.user.id
    hu = get_object_or_404(HoseUser, pk=hoser_id)
    other_id = hu.id
    ha = HoseAssociation.objects. \
        filter(
            (Q(first_end=user_id) and Q(second_end=other_id))
            or
            (Q(first_end=other_id) and Q(second_end=user_id))
        )
    context = {
        'hoser_username': hu.username,
        'has_hose': False,
        'hose_association_id': -1,
        'hose_association_name': -1,
    }
    if len(ha) > 0:
        context['has_hose'] = True
        context['hose_association_id'] = ha[0].id
        context['hose_association_name'] = ha[0].hose_name
    return render(request, template_name, context)


def show_hose(request, hose_id):
    user_id = request.user.id
    ha = get_object_or_404(HoseAssociation, pk=hose_id)
    if user_id != ha.first_end.id and user_id != ha.second_end.id:
        return Http404('<h1>Hose was not found</h1>')
    template_name = 'hose_usage/show_hose.html'
    other_end = ha.second_end
    if user_id == ha.second_end.id:
        other_end = ha.first_end
    songs = HoseContent.objects.filter(hose_from__id=ha.id).order_by('-time_added').all()
    context = {
        'hose_name': ha.hose_name,
        'time_created': ha.time_created,
        'time_last_update': ha.time_last_update,
        'other_username': other_end.username,
        'other_id': other_end.id,
        'songs': songs
    }
    return render(request, template_name, context)


def ask_for_hose_creation(request):
    return HttpResponse('Asking Hose with:')


class SignUp(generic.CreateView):
    """Signup view"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
