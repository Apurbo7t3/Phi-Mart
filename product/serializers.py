from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product,Review,ProductImage
from django.contrib.auth import get_user_model

# class CategorySerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     name=serializers.CharField()
#     description=serializers.CharField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','product_count']
    product_count=serializers.IntegerField()        


# class ProductSerilizer(serializers.Serializer):
#     id=serializers.IntegerField()
#     name=serializers.CharField()
#     unit_price=serializers.DecimalField(max_digits=10, decimal_places=2,source='price')
#     price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
#     # category=serializers.PrimaryKeyRelatedField(
#     #     queryset=Category.objects.all()
#     # )
#     # category=serializers.StringRelatedField()
#     # category=CategorySerializer()
#     category=serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name='category-list'
#     )
#     def calculate_tax(self,product):
#         return round(product.price*Decimal(1.1),2)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = ['id', 'name', 'description', 'price',
                  'stock', 'category', 'price_with_tax'] 

    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self,product):
        return round(product.price*Decimal(1.1),2)


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields=[
            'id', 'user', 'product', 'comment', 'ratings',
        ]
        read_only_fields = ['user', 'product']
        
    def create(self,validated_data):
        product_pk=self.context['product_pk']
        return Review.objects.create(product_id=product_pk,**validated_data)
    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']