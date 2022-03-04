from rest_framework import serializers

from .models import Bicycle, Media, Order, OrderDetail


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('image', )

    def to_representation(self, instance: Media):
        request = self.context.get('request')
        domain = request.build_absolute_uri('/')[:-1]
        photo_url = instance.image.url
        return domain + photo_url


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
    bicycle_image = serializers.SerializerMethodField()
    bicycle_price = serializers.DecimalField(
        decimal_places=2,
        max_digits=7
    )

    def get_bicycle_image(self, instance):
        request = self.context.get('request')
        domain = request.build_absolute_uri('/')[:-1]
        photo_url = instance.bicycle.cover_image.url
        return domain + photo_url

    class Meta:
        model = OrderDetail
        fields = ('start_date', 'end_date', 'bicycle_name',
                  'bicycle_price', 'bicycle_image', 'flashlight',
                  'helmet', 'lock')


class BicycleListSerializer(serializers.ModelSerializer):

    brand_name = serializers.CharField(source='brand__name')
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    cover_image = serializers.SerializerMethodField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = Bicycle
        fields = ('id', 'name', 'cover_image', 'wheel_diameter', 'brand_name', 'price', 'start_date', 'end_date')

    def get_cover_image(self, bicycle):
        request = self.context.get('request')
        domain = request.build_absolute_uri('/')[:-1]
        photo_url = bicycle.get('cover_image')
        return domain + '/media/' + photo_url


class OrderSerializer(serializers.ModelSerializer):

    bicycles = OrderDetailSerializer(many=True, source='order_details')
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('id', 'bicycles', 'created_date', 'total_sum', 'status')


class OrderCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
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
                bicycle_price=bicycle.get('bicycle_price'),
                flashlight=bicycle.get('flashlight', False),
                helmet=bicycle.get('helmet', False),
                lock=bicycle.get('lock', False),
            )

        return order

    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data