from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View

from .models import Category, UserClass, Product, Order, SelectedProduct
from .mixins import SelectionMixin
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_selection


class BaseView(SelectionMixin, View):
    """
    Representation of main page
    """
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'selection': self.selection
        }
        return render(request, 'base.html', context)


class ProductDetailView(SelectionMixin, DetailView):
    """
    Representation of product details in web
    """

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Function gets context - content type of models, selection on request"""
        context = super(ProductDetailView, self).get_context_data()
        context['selection'] = self.selection
        return context


class CategoryDetailView(SelectionMixin, DetailView):
    """
    Class is used to represent product in category page
    """
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Function gets context - selection on request"""
        context = super().get_context_data()
        context['selection'] = self.selection
        return context


class AddToSelectionView(SelectionMixin, View):
    """
    Class is used to represent
    adding products to Selection
    """

    def get(self, request, *args, **kwargs):
        """
        Function makes redirect to Selection if product was added.
        At the end of operation withdraw message.
        """
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        selected_product, created = SelectedProduct.objects.get_or_create(
            user=self.selection.owner,
            selected_item=self.selection,
            product=product
        )
        if created:
            self.selection.products.add(selected_product)
        recalc_selection(self.selection)
        messages.add_message(request, messages.INFO, 'Product successfully added')
        return HttpResponseRedirect('/selection/')


class RemoveFromSelectionView(SelectionMixin, View):
    """
    Class is used to represent
    Selection when product was removed
    """

    def get(self, request, *args, **kwargs):
        """
        Function makes redirect to Selection if product was removed.
        At the end of operation withdraw message.
        """
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        selected_product = SelectedProduct.objects.get(
            user=self.selection.owner,
            selected_item=self.selection,
            product=product
        )
        self.selection.products.remove(selected_product)
        selected_product.delete()
        recalc_selection(self.selection)
        messages.add_message(request, messages.INFO, 'Product successfully removed')
        return HttpResponseRedirect('/selection/')


class ChangeQtyView(SelectionMixin, View):
    """
    Class is used to represent Selection and
    manage button to change item quantity
    """

    def post(self, request, *args, **kwargs):
        """
        Function makes redirect to Selection if product quantity was changed.
        At the end of operation withdraw message.
        """
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        selected_product = SelectedProduct.objects.get(
            user=self.selection.owner,
            selected_item=self.selection,
            product=product
        )
        qty = int(request.POST.get('qty'))
        selected_product.qty = qty
        selected_product.save()
        recalc_selection(self.selection)
        messages.add_message(request, messages.INFO, 'Quantity successfully changed')
        return HttpResponseRedirect('/selection/')


class SelectionView(SelectionMixin, View):
    """Representation of Selection page"""

    def get(self, request, *args, **kwargs):
        """Renders Selection template on request"""
        categories = Category.objects.all()
        context = {
            'selection': self.selection,
            'categories': categories
        }
        return render(request, 'selection.html', context)


class CheckoutView(SelectionMixin, View):
    """
    Class is used to represent in Selection go process to order
    """
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'selection': self.selection,
            'categorise': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(SelectionMixin, View):
    """"
    Class is used to represent order with selected items.
    When order makes message of status withdraw
    """
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        user = UserClass.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = user
            new_order.order_type = form.cleaned_data.get('order_type')
            new_order.order_date = form.cleaned_data.get('order_date')
            new_order.comment = form.cleaned_data.get('comment')
            new_order.save()
            self.selection.in_order = True
            self.selection.save()
            new_order.selection = self.selection
            new_order.save()
            user.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Order is done')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout')


class LoginView(SelectionMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'selection': self.selection
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form, 'selection': self.selection}
        return render(
            request,
            'login.html',
            context
        )


class RegistrationView(SelectionMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form': form,
            'categorise': categories,
            'selection': self.selection
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            # new_user.organization = form.cleaned_data['organization']
            new_user.position = form.cleaned_data['position']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            UserClass.objects.create(
                user=new_user,

            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
            'selection': self.selection
        }
        return render(request, 'registration.html', context)


class ProfileView(SelectionMixin, View):

    def get(self, request, *args, **kwargs):
        user = UserClass.objects.get(user=request.user)
        orders = Order.objects.filter(user=user,).order_by('-created_at')
        categories = Category.objects.all()
        context = {
            'orders': orders,
            'selection': self.selection,
            'categories': categories
        }
        return render(
            request,
            'profile.html',
            context
        )
