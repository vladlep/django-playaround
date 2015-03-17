from rest_framework import status, permissions, viewsets
from .models import Cost
from .api_serializers import CostSerializerV2


class CostViewSet(viewsets.ModelViewSet):

    queryset = Cost.objects.all()
    serializer_class = CostSerializerV2
