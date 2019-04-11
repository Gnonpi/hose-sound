from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from hose_usage.serializers import HoseUserSerializer, HoseAssociationSerializer, HoseContentSerializer
from hose_usage.forms import CustomUserCreationForm, UploadSongForm
from hose_usage.models import HoseUser, HoseAssociation, HoseContent, AssociationDemand
import hose_usage.permissions as hose_permissions


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
            nb_songs = HoseContent.objects.filter(hose_from__id=ha.id).count()
            ha_dict['nb_songs'] = nb_songs
            if ha_dict['first_end_id'] == user_id:
                ha_dict['other_user_username'] = ha_dict['second_end_username']
            else:
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
                ha_dict['other_user_username'] = ha_dict['second_end_username']
            else:
                ha_dict['other_user_username'] = ha_dict['first_end_username']
            ha_dict['nb_songs'] = nb_songs
            results.append(ha_dict)
        return results


def browse_hosers(request):
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
    """Show the details of one Hose"""
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


def ask_for_hose_creation(request, hoser_id):
    """Ask another Hoser to create a Hose"""
    user_demands = AssociationDemand.objects.filter(sender=request.user).count()
    if user_demands > AssociationDemand.MAX_DEMANDS_SENT:
        messages.error(request, 'You already send too many demands')
        return redirect(reverse('h:show_hoser'))
    other = get_object_or_404(HoseUser, pk=hoser_id)
    demand = AssociationDemand(
        sender=request.user,
        receiver=other,
    )
    demand.save()
    messages.success(request, f'Demand sent to {other.username}')
    return redirect(reverse('h:home'))


def _delete_caduced_demands(list_demands):
    """Remove caduced demands from the list"""
    filtered_demands = []
    for demand in list_demands:
        if demand.is_caduced():
            demand.delete()
        else:
            filtered_demands.append(demand)
    return filtered_demands


def see_hose_demands(request):
    """See all sent or received demands"""
    sent_demands = AssociationDemand.objects.filter(sender=request.user). \
        order_by('-time_sent').all()
    received_demands = AssociationDemand.objects.filter(receiver=request.user). \
        order_by('-time_sent').all()
    sent_demands = _delete_caduced_demands(sent_demands)
    received_demands = _delete_caduced_demands(received_demands)

    template_name = 'hose_usage/see_demands.html'
    context = {
        'sent_demands': sent_demands,
        'received_demands': received_demands,
    }
    return render(request, template_name, context)


def confirm_hose_creation(request, demand_id):
    """Let a user confirm the creation of a Hose with another one after receiving demand"""
    demand = get_object_or_404(AssociationDemand, pk=demand_id)
    if demand.is_caduced():
        messages.error(request, 'Demand has caduced')
        return redirect(reverse('h:home'))
    # Create a new Hose with first end the current user
    try:
        second = HoseUser.objects.get(pk=demand.sender.id)
    except HoseUser.DoesNotExist as ex:
        messages.error(request, 'Hoser accound has been deleted')
        return redirect(reverse('h:home'))
    else:
        ha = HoseAssociation(
            first_end=request.user,
            second_end=second,
            hose_name='-'.join([request.user.username, second.username])
        )
        ha.save()
        return redirect(reverse('h:show_hose', kwargs={'hose_id': ha.id}))


def cancel_hose_creation(request, hoser_id):
    """Delete the demand to create a Hose"""
    try:
        receiver = HoseUser.objects.filter(pk=hoser_id).first()
    except HoseUser.DoesNotExist as ex:
        messages.error(request, 'Hoser account has been deleted')
        return redirect(reverse('h:home'))
    else:
        demand = get_object_or_404(AssociationDemand, sender=request.user, receiver=receiver)
        demand.delete()
        messages.info('Demand was canceled')
        return redirect(reverse('h:home'))


def handle_uploaded_file(file):
    with open('./filename', 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


def upload_song(request, hose_id):
    ha = get_object_or_404(HoseAssociation, pk=hose_id)
    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            content = HoseContent(
                hose_from=ha,
                uploader=request.user,
                name=request.FILES['files'].name,
                file_field=request.FILES['file'],
            )
            content.save()
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponse('Upload is ok.')


class SignUp(generic.CreateView):
    """Signup view"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


## REST views
class HoseUserList(APIView):
    permission_classes = (permissions.IsAuthenticated,
                          hose_permissions.IsOwnerOf)

    def get(self, request, format=None):
        users = HoseUser.objects.all()
        users_serialized = HoseUserSerializer(users, many=True)
        return Response(users_serialized.data)

    def post(self, request, format=None):
        serialized = HoseUserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.error, status=status.HTTP_400_BAD_REQUEST)


class HoseUserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,
                          hose_permissions.IsOwnerOf)

    def get_object(self, pk):
        user = get_object_or_404(HoseUser, pk=pk)
        return user

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serialized = HoseUserSerializer(user)
        return Response(serialized.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serialized = HoseUserSerializer(user, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HoseAssociationDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,
                          hose_permissions.IsOwnerOf)

    def get_object(self, pk):
        hose = get_object_or_404(HoseAssociation, pk=pk)
        return hose

    def get(self, request, pk, format=None):
        hose = self.get_object(pk=pk)
        serialized = HoseAssociationSerializer(hose, context={'request': request})
        return Response(serialized.data)

    def post(self, request, format=None):
        serialized = HoseAssociationSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.error, status=status.HTTP_400_BAD_REQUEST)

class HoseContentList(APIView):
    permission_classes = (permissions.IsAuthenticated, hose_permissions.IsOwnerOf,)

    def get(self, request, format=None):
        accessible_hose = HoseAssociation.objects.filter(
            Q(first_end=request.user) | Q(second_end=request.user)
        )
        contents = HoseContent.objects.filter(hose_from__in=accessible_hose).all()
        contents_serialized = HoseContentSerializer(contents, many=True)
        return Response(contents_serialized.data, status=status.HTTP_200_OK)
