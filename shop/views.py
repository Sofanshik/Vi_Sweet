from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.views import View
from .forms import *
from .models import *
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


cursor = connection.cursor()


def main_page(request):
    return render(request, 'main_page.html')


class CatalogOfCakesListView(ListView):
    cursor.execute("SELECT * FROM shop_cake")
    catalog_cakes = dictfetchall(cursor)
    model = Cake
    queryset = catalog_cakes
    template_name = 'catalog_of_cakes.html'
    context_object_name = 'cakes'


class BlogItemsListView(ListView):
    cursor.execute("select BL.id, BL.title, BL.description, CN.name, CN.phone_number, CN.address from shop_blog as BL left join  shop_confectioner as CN on BL.confectioner_id = CN.id")
    blog_items = dictfetchall(cursor)
    model = Blog
    queryset = blog_items
    template_name = 'blog_list.html'
    context_object_name = 'blog_items'


class ReviewsListView(ListView):
    cursor.execute("select BL.id, BL.mark, BL.text, CN.first_name, CN.username, CN.last_name from shop_review as BL left join  shop_customer as CN on BL.customer_id = CN.id")
    reviews = dictfetchall(cursor)
    model = Review
    queryset = reviews
    template_name = 'reviews.html'
    context_object_name = 'reviews'


def get_customer_profile(request):
    if username := request.user.username:
        return render(request, 'customer_profile.html')


class RegistrationCustomer(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomerCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomerCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main_page_url')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class CreateReviewsCreateView(CreateView):
    form_class = CreateReviewForm
    template_name = 'create_review.html'
    http_method_names = ['post', 'get']
    success_url = 'reviews'

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)


class CreateOrderView(CreateView):
    model = OrderC
    form_class = CreateOrderForm
    template_name = 'create_order.html'
    success_url = 'profile/'
    http_method_names = ['post', 'get']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)


def get_customer_for_order(customer_id):
    cursor.execute("SELECT * FROM shop_orderc WHERE customer_id=%i"%customer_id)
    return dictfetchall(cursor)


class OrderListView(LoginRequiredMixin, ListView):
    model = OrderC
    template_name = 'list_of_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return get_customer_for_order(self.request.user.id)


class GetLove(ListView):
    cursor.execute("SELECT * FROM (SELECT BL.status, CN.title, CN.price from shop_orderc_cakes as OC inner join shop_orderc as BL on BL.id = OC.orderc_id inner join shop_cake CN on OC.cake_id = CN.id) where status = 'Paid' or status = 'DONE' ORDER BY price desc;")
    blog_items = dictfetchall(cursor)
    queryset = blog_items
    template_name = 'get_love.html'
    context_object_name = 'get_loves'
