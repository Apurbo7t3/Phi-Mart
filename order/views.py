from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from order.models import Cart,CartItem,Order,OrderItem
from order.serializers import CartSerializer,CartItemSerializer,AddItemSerializer,UpdateSerializer,OrderSerializer,CreateOrderSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReaOnly
from order.serializers import UpdateOrderSerializer,EmptySerializer
from order.services import CreateOrderService
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.


class CartViewSet(GenericViewSet,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin):
    permission_classes=[IsAuthenticated]
   
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.filter(user=self.request.user)
    
    serializer_class=CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','patch','post','delete']
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))
    def get_serializer_context(self):
        return {'cart_id':self.kwargs.get('cart_pk')}
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddItemSerializer
        if self.request.method == 'PATCH':
            return UpdateSerializer
        else:
            return CartItemSerializer
        
    
class OrderViewSet(ModelViewSet):
    http_method_names=['patch','delete','post','get','head','options']

    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        order=self.get_object()
        CreateOrderService.cancel_order(order=order,user=request.user)
        return Response({'status':'Order canceled'})

    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order=self.get_object()
        serializer=UpdateOrderSerializer(order,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':f'Status updated Successfully to {request.data["status"]}'})

    def get_permissions(self):
        if self.action in ['update_status',"destroy"]:
            return [IsAdminOrReaOnly()]
        return [IsAuthenticated()]
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        if self.action=='create':
            return CreateOrderSerializer
        if self.request.method=='update_status':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id,'user':self.request.user}
    
    
    