from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category,Review,ProductImage
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImageSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from product.filters import ProductFilter
from product.paginations import DefaultPagination
from api.permissions import IsAdminOrReaOnly
from product.permissions import IsAuthorOrRandom
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class ProductViewSet(ModelViewSet):
        """
        API Endpoint creating updating,Reading and deleting product
            -Only admin can read write and delete product
            -User can can only view product with or without log in
        """

        @swagger_auto_schema(
                operation_summary='Used by admin to create product',
                operation_description='only authorized Admin can create product',
                responses={
                        400:'bad Request'
                }
        )
        def create(self, request, *args, **kwargs):
                """
                Only Admin can create product
                """
                return super().create(request, *args, **kwargs)
        permission_classes=[IsAdminOrReaOnly]
        queryset=Product.objects.all()
        serializer_class=ProductSerializer
        filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
        search_fields=['name','description']
        ordering_fields=['price','created_at']
        pagination_class= DefaultPagination
        # filterset_fields=['category_id','price']
        filterset_class= ProductFilter
        # def get_queryset(self):
        #     queryset=Product.objects.all()
        #     category_id=self.request.query_params.get('category_id')
        #     if category_id is not None:
        #             queryset=Product.objects.filter(category_id=category_id)
        #     return queryset

class ProductImageViewSet(ModelViewSet):
       serializer_class=ProductImageSerializer
       permission_classes=[IsAdminOrReaOnly]
       def get_queryset(self):
           return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
       
       def perform_create(self, serializer):
               serializer.save(product_id=self.kwargs.get('product_pk'))
        


class CategoryViewSet(ModelViewSet):
        queryset=Category.objects.annotate(product_count=Count('products')).all()
        serializer_class=CategorySerializer






class ReviewViewSet(ModelViewSet):
        permission_classes=[IsAuthorOrRandom]
        serializer_class = ReviewSerializer
        def get_queryset(self):
            return Review.objects.filter(product_id=self.kwargs.get('product_pk')).all()
        def get_serializer_context(self):
                return {'product_pk':self.kwargs.get('product_pk')}
        
        def perform_create(self, serializer):
                serializer.save(user=self.request.user)
        def perform_update(self, serializer):
                serializer.save(user=self.request.user)
        





# @api_view(['GET','PUT','DELETE'])
# def view_specific_product(request,pk):
#         if request.method=='GET':
#                 product=get_object_or_404(Product,pk=pk)
#                 product_dict=ProductSerializer(product)
#                 return Response(product_dict.data)
#         if request.method=='PUT':
#                 product=get_object_or_404(Product,pk=pk)
#                 product_dict=ProductSerializer(product,data=request.data)
#                 product_dict.is_valid(raise_exception=True)
#                 product_dict.save()
#                 return Response(product_dict.data)
#         if request.method=='DELETE':
#                 product=get_object_or_404(Product,pk=pk)
#                 copy=product
#                 product.delete()
#                 product_dict=ProductSerializer(copy)
#                 return Response(product_dict.data,status=status.HTTP_204_NO_CONTENT)


class ViewSpecificProduct(APIView):
       def get(self,request,pk):
                product=get_object_or_404(Product,pk=pk)
                product_dict=ProductSerializer(product)
                return Response(product_dict.data)
       def put(self,request,pk):
                product=get_object_or_404(Product,pk=pk)
                product_dict=ProductSerializer(product,data=request.data)
                product_dict.is_valid(raise_exception=True)
                product_dict.save()
                return Response(product_dict.data)
       def delete(self,request,pk):
                product=get_object_or_404(Product,pk=pk)
                copy=product
                product.delete()
                product_dict=ProductSerializer(copy)
                return Response(product_dict.data,status=status.HTTP_204_NO_CONTENT)

class ProductDetails(RetrieveUpdateDestroyAPIView):
        queryset=Product.objects.all()
        serializer_class=ProductSerializer

# @api_view(['GET','POST'])
# def view_products(request):
#         if request.method=='GET':
#                 product=get_list_or_404(Product)
#                 product_dict=ProductSerializer(product,many=True)
#                 return Response(product_dict.data)
#         if request.method=='POST':
#                serializer=ProductSerializer(data=request.data)
#                if serializer.is_valid():
#                       serializer.save()
#                       return Response(serializer.data,status=status.HTTP_201_CREATED)
#                else:
#                       return Response(status=status.HTTP_400_BAD_REQUEST)



# class ViewProducts(APIView):
#         def get(self,request):
#                 product=get_list_or_404(Product)
#                 product_dict=ProductSerializer(product,many=True)
#                 return Response(product_dict.data)
#         def post(self,request):
#                 serializer=ProductSerializer(data=request.data)
#                 if serializer.is_valid():
#                         serializer.save()
#                         return Response(serializer.data,status=status.HTTP_201_CREATED)
#                 else:
#                         return Response(status=status.HTTP_400_BAD_REQUEST)



class ProductList(ListCreateAPIView):

        queryset=queryset = Product.objects.all()
        serializer_class=ProductSerializer

        """ For logical implementation """
        # def get_queryset(self):
        #     return get_list_or_404(Product)
        # def get_serializer_class(self):
        #         return ProductSerializer
        # def get_serializer_context(self):
        #         return {'request':self.request}
        

# @api_view()
# def view_category(request):
#         category=Category.objects.annotate(product_count=Count('products')).all()
#         category_dict=CategorySerializer(category,many=True)
#         return Response(category_dict.data)


class ViewCategories(APIView):
        def get(self,request):
                category=Category.objects.annotate(product_count=Count('products')).all()
                category_dict=CategorySerializer(category,many=True)
                return Response(category_dict.data)
        def post(self,request):
                serializer=CategorySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)



# @api_view()
# def view_specific_category(request,pk):
#      category=get_object_or_404(Category,pk=pk)
#     category = get_object_or_404(
#         Category.objects.annotate(product_count=Count('products')), 
#         pk=pk
#     )
#     serialize=CategorySerializer(category)
#     return Response(serialize.data)



class ViewSpecificCategory(APIView):
        def get(self,request,pk):
                category=get_object_or_404(Category,pk=pk)
                serializer=CategorySerializer(category)
                return Response(serializer.data)
        def put(self,request,pk):
                category=get_object_or_404(Category,pk=pk)
                serializer=CategorySerializer(category,data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        def delete(self,request,pk):
                category=get_object_or_404(Category,pk=pk)
                copy=category
                category.delete()
                return Response(CategorySerializer(copy).data,status=status.HTTP_204_NO_CONTENT)
        

class CategoryDetails(RetrieveUpdateDestroyAPIView):
        queryset=Category.objects.annotate(product_count=Count('products')).all()
        serializer_class=CategorySerializer