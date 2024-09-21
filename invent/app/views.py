from django.shortcuts import render
from rest_framework import viewsets
from .serializer import ProductoSerializer
from .models import Producto
from django.http import HttpResponse


# Create your views here.
class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    
# Create your views here.
def index(request):
    return HttpResponse(f"<h1>Index {request.tenant}<h1>")