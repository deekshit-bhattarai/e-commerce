from rest_framework import generics
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from product.models import ProductVariant
from .serializers import ProductAdminSerializer

class ProductVariantAdminView(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    queryset = ProductVariant.objects.all()   
    serializer_class = ProductAdminSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        product = request.data 
        serializer = ProductAdminSerializer(product)
        serializer.save()

        

