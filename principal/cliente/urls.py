from django.urls import path

from .views import ClienteCreateView
from .views import ClienteListView, ClienteUpdateView

app_name = 'cliente'
urlpatterns = [
    #path('listar', ClienteListView.as_view(), name="list"),
    #path('<slug:slug>/', EmpresaDetailView.as_view(), name="empresa.empresa_detail"),
    path('cadastrar/', ClienteCreateView.as_view(), name="create"),
    path('listar/', ClienteListView.as_view(), name="list"),
    path('alterar/<slug:slug>/', ClienteUpdateView.as_view(), name="update"),
    
]