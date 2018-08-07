from django.contrib.auth.models import Group  # , User
from rest_framework import serializers
from users.models import User
from core.models import SpidersBaseSource


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SpidersBaseSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpidersBaseSource
        fields = ('url', 'hash_id', 'city', 'url_type', 'url_source', 'update_time')


