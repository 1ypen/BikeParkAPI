from datetime import datetime

from django.contrib.postgres.search import SearchQuery
from django.db.models import OuterRef, Subquery, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .models import Bicycle, Order, Price, OrderDetail
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
    filterset_fields = ['size', 'type', 'material']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        query = self.request.GET.get("q")

        price = Price.objects.filter(
            bicycle=OuterRef('pk'),
            is_current=True
        )
        rental_days = OrderDetail.objects.filter(
            bicycle=OuterRef('pk'),
            end_date__gte=datetime.now()
        )

        if query:
            bicycles_queryset = Bicycle.objects.filter(content_search=SearchQuery(query), is_active=True)
        else:
            bicycles_queryset = Bicycle.objects.filter(is_active=True)

        bicycles_queryset = (
            bicycles_queryset
                .filter(is_active=True)
                .annotate(price=Subquery(price.values('price')),
                          start_date=Subquery(rental_days.values('start_date')),
                          end_date=Subquery(rental_days.values('end_date')))
                .select_related('brand')
                .values('id', 'name', 'brand__name', 'price', 'cover_image', 'wheel_diameter', 'start_date', 'end_date')
        )

        return bicycles_queryset

    def get_serializer_class(self):
        return BicycleListSerializer


class OrderListAPI(ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        query = self.request.GET.get("query")

        queryset = (
            Order.objects.all()
                .prefetch_related('order_details')
        )
        if query == 'completed':
            queryset = queryset.filter(status='CO')
        elif query == 'unfulfilled':
            queryset = queryset.filter(~Q(status='CO'))

        return queryset


class OrderCreateAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer
