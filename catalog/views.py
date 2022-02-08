from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend


from .models import Bicycle, Order
from .serializers import BicycleDetailSerializer, BicycleListSerializer, OrderCreateSerializer, OrderSerializer


class BicycleDetailAPI(RetrieveAPIView):
    """
    get detailed information about the bike
    """

    def get_queryset(self):
        bicycle_queryset = Bicycle.objects.filter(is_active=True)
        return bicycle_queryset

    def get_serializer_class(self):
        serializer_bicycle = BicycleDetailSerializer
        return serializer_bicycle


class BicycleListAPI(ListAPIView):
    """
    get information about all bikes
    """

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['size', 'type', 'brand__name']

    def get_queryset(self):
        bicycles_queryset = Bicycle.objects.filter(is_active=True) \
            .select_related('brand')

        return bicycles_queryset

    def get_serializer_class(self):
        return BicycleListSerializer


class OrderListAPI(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().\
        prefetch_related('order_details')\



class OrderCreateAPI(CreateAPIView):
    serializer_class = OrderCreateSerializer

