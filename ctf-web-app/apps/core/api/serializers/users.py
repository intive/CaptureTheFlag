from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.core.models import PortalUser, Character

__author__ = 'mkr'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('type', 'total_time', 'total_score', 'health', 'level')


class PortalUserSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(read_only=True)

    def save_object(self, obj, **kwargs):
        super(PortalUserSerializer, self).save_object(obj, **kwargs)
        try:
            player_group = Group.objects.get_by_natural_key("Player")
        except Group.DoesNotExist, e:
            # todo: add logger in this place
            raise e

        if getattr(self, "password_was_set", False):
            obj.set_password(obj.password)

        player_group.user_set.add(obj)
        obj.save()

    class Meta:
        model = PortalUser
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'nick', 'characters')


class PortalUserListSerializer(serializers.ModelSerializer):
    characters = CharacterSerializer(read_only=True)

    class Meta:
        model = PortalUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'nick', 'characters')