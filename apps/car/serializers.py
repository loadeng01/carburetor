from rest_framework import serializers
from .models import Car, CarImages


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImages
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Car
        fields = ('id', 'owner', 'title', 'year', 'category', 'color', 'mileage', 'volume', 'fuel',
                  'engine', 'drive_unit', 'kpp', 'str_wheel', 'preview', 'city', 'price', 'description',
                  'created_at', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        car = Car.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            CarImages.objects.create(image=image, car=car)
        return car

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['owner_phone_number'] = repr.get('owner.phone_number')
        return repr


class CarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'preview', 'title', 'year', 'mileage', 'price')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        data = {
            'id': repr['id'],
            'preview': repr['preview'],
            'title': repr['title'],
            'year': repr['year'],
            'mileage': repr['mileage'],
            'price': repr['price']
        }
        return data
