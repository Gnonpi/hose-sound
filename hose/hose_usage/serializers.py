from django.db.models import Q
from rest_framework import serializers

from hose_usage.models import HoseUser, HoseAssociation, HoseContent


class HoseUserSerializer(serializers.ModelSerializer):
    # TODO: replace with PrimaryKeyRelatedField
    accessible_hoses = serializers.SerializerMethodField('get_hoses')

    def get_hoses(self, user):
        qs = HoseAssociation.objects.filter(Q(first_end=user) | Q(second_end=user)).all()
        hoses_serialized = HoseAssociationSerializer(instance=qs, many=True)
        return hoses_serialized.data

    class Meta:
        model = HoseUser
        fields = ('id', 'username', 'accessible_hoses')  # not showing email


class HoseAssociationSerializer(serializers.ModelSerializer):
    first_end_username = serializers.ReadOnlyField(source='first_end.username')
    second_end_username = serializers.ReadOnlyField(source='second_end.username')
    hose_origin = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = HoseAssociation
        fields = ('id', 'first_end', 'second_end',
                  'first_end_username', 'second_end_username',
                  'hose_name', 'time_created', 'time_last_update',
                  'hose_origin')


class HoseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoseContent
        fields = ('id', 'hose_from', 'uploader',
                  'name', 'time_added', 'times_listened')
