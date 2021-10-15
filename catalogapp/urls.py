from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    SelectionView,
    AddToSelectionView,
    RemoveFromSelectionView,
    ChangeQtyView,
    CheckoutView,
    MakeOrderView,
    LoginView,
    RegistrationView,
    ProfileView
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('selection/', SelectionView.as_view(), name='selection'),
    path('add-to-selection/<str:slug>/', AddToSelectionView.as_view(), name='add_to_selection'),
    path('remove-from-selection/<str:slug>/',
         RemoveFromSelectionView.as_view(),
         name='remove_from_selection'
         ),
    path('change-qty/<str:slug>/', ChangeQtyView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('makeorder/', MakeOrderView.as_view(), name='makeorder'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile')
]
