import warnings
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.core.api.serializers import characters, users
from apps.core.models import PortalUser, Character

__author__ = 'mkr'


@api_view(['GET'])
def profile(request):
    # user = request.user
    user = PortalUser.objects.first()
    serializer = users.PortalUserSerializer(user)

    if "password" in serializer.data:
            serializer.data.pop("password")

    return Response(serializer.data)


class PortalUserViewSet(viewsets.ModelViewSet):
    serializer_class = users.PortalUserSerializer
    model = PortalUser
    object = None
    object_list = None

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)

        if "password" in serializer.data:
            serializer.data.pop("password")

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())

        # Default is to allow empty querysets.  This can be altered by setting
        # `.allow_empty = False`, to raise 404 errors on empty querysets.
        if not self.allow_empty and not self.object_list:
            warnings.warn(
                'The `allow_empty` parameter is due to be deprecated. '
                'To use `allow_empty=False` style behavior, You should override '
                '`get_queryset()` and explicitly raise a 404 on empty querysets.',
                PendingDeprecationWarning
            )
            class_name = self.__class__.__name__
            error_msg = self.empty_error % {'class_name': class_name}
            raise Http404(error_msg)

        # Switch between paginated or standard style responses
        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)

        return Response(serializer.data)


class CharacterViewSet(viewsets.ModelViewSet):
    serializer_class = characters.CharacterSerializer
    model = Character