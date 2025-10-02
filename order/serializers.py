from rest_framework import serializers
from order.models import Cart,CartItem
from product.models import Product
from order.models import Order,OrderItem
from order.services import CreateOrderService


class EmptySerializer(serializers.Serializer):
    pass


class AddItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Product with id {value} does not exists")
        return value

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','description','price']


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(
        method_name='get_total_price'
    )
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']
    
    def get_total_price(self,item:CartItem):
        return item.quantity*item.product.price



class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model= Cart
        fields=['id','user','items','total_price']
        read_only_fields=['user']

    def get_total_price(self,cart:Cart):
        return sum([ item.quantity*item.product.price for item in cart.items.all() ])
    

class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()
    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found')
        if not CartItem.objects.filter(cart_id=cart_id):
            raise serializers.ValidationError('Cart is empty')
        return cart_id
    def create(self, validated_data):
        cart_id=self.validated_data['cart_id']
        user_id=self.context['user_id']
        order=CreateOrderService.create_order(user_id=user_id,cart_id=cart_id)
        return order
    def to_representation(self, instance):
        return OrderSerializer(instance).data
    

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']
        read_only_fields=['user','items','total_price']

    # def update(self, instance, validated_data):
    #     if self.request.user.is_staff:
    #         new_status=validated_data['status']
    #         user=self.context['user']
    #         if new_status == Order.CANCELED:
    #             return CreateOrderService.cancel_order(order=instance,user=user)
    #         if not user.is_staff:
    #             raise serializers.ValidationError('You Dont have Permission of this')
    #     return super().update(instance, validated_data)

class OrderItemserializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','price','quantity','total_price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemserializer(many=True)
    class Meta:
        model=Order
        fields=['id','user','status','items','total_price','created_at']