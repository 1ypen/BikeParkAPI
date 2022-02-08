from datetime import datetime

from rest_framework import serializers

from .models import Bicycle, Media, Order, OrderDetail


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('image', )

    def to_representation(self, instance: Media):
        return instance.image.url


class BicycleDetailSerializer(serializers.ModelSerializer):

    material = serializers.CharField(source='get_material_display')
    type = serializers.CharField(source='get_type_display')
    size = serializers.CharField(source='get_size_display')
    brand = serializers.CharField(source='brand.name')
    images = MediaSerializer(many=True)

    class Meta:
        model = Bicycle
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):

    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    bicycle_name = serializers.CharField(source='bicycle.name')
    bicycle_price = serializers.DecimalField(
        decimal_places=2,
        max_digits=7
    )

    class Meta:
        model = OrderDetail
        fields = ('start_date', 'end_date', 'bicycle_name', 'bicycle_price')


class BicycleListSerializer(serializers.ModelSerializer):

    brand_name = serializers.CharField(source='brand.name')
    price = serializers.SerializerMethodField(method_name='get_price')
    rental_days = serializers.SerializerMethodField(method_name='get_rental_days')

    class Meta:
        model = Bicycle
        fields = ('id', 'name', 'cover_image', 'wheel_diameter', 'brand_name', 'price', 'rental_days')

    def get_price(self, bicycle_obj: Bicycle):
        return bicycle_obj.prices.get(is_current=True).price

    def get_rental_days(self, bicycle_obj: Bicycle):
        order_details = bicycle_obj.order_details.filter(end_date__gte=datetime.now())
        return OrderDetailSerializer(order_details, many=True).data


class OrderSerializer(serializers.ModelSerializer):

    bicycles = OrderDetailSerializer(many=True, source='order_details')

    class Meta:
        model = Order
        fields = ('bicycles', )


class OrderCreateSerializer(serializers.ModelSerializer):

    bicycles = serializers.ListField()

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        # get bicycles from json
        bicycles = validated_data.pop('bicycles')
        
        # create Order
        order = Order.objects.create(**validated_data)
        
        # create OrderDetail
        for bicycle in bicycles:
            OrderDetail.objects.create(
                order=order,
                bicycle_id=bicycle.get('id'),
                start_date=bicycle.get('start_date'),
                end_date=bicycle.get('end_date'),
                bicycle_price=bicycle.get('bicycle_price')
            )

        return order

    def to_representation(self, instance):
        return OrderSerializer(instance).data