from django.urls import path, include
from .views import *
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main_page, name='main_page_url'),
    path('catalog_of_cakes', CatalogOfCakesListView.as_view(), name='catalog_cakes_url'),
    path('blog', BlogItemsListView.as_view(), name='blog_url'),
    path('create_review', CreateReviewsCreateView.as_view(), name='create_review_url'),
    path('reviews', ReviewsListView.as_view(), name='reviews_url'),
    path('registration', RegistrationCustomer.as_view(), name='registration_url'),
    path('profile/', views.get_customer_profile, name='profile_url'),
    path('create_orders', CreateOrderView.as_view(), name='create_order_url'),
    path('customer/', include('django.contrib.auth.urls')),
    path('list_of_order', OrderListView.as_view(), name='list_of_orders_url'),
    path('get_love', GetLove.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
