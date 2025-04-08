from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Customer, InventoryMovement, Sale, SaleItem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from django.db import models

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.content_type == 'application/json':
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            return redirect('dashboard')
        else:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Invalid credentials'}, status=401)
            messages.error(request, 'Usuário ou senha inválidos')
    
    return render(request, 'core/login.html')


def register_view(request):
    return render(request, 'core/register.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'detail': 'Successfully logged out'}, status=200)
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

from rest_framework_simplejwt.tokens import RefreshToken

def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            user = User.objects.create_user(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'User created successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required(login_url='/login/')
def dashboard_view(request):
    today = timezone.now().date()
    context = {
        'products_count': Product.objects.count(),
        'customers_count': Customer.objects.count(),
        'today_sales_count': Sale.objects.filter(date__date=today).count(),
        'low_stock_count': Product.objects.filter(stock_quantity__lte=models.F('minimum_stock')).count(),
        'recent_sales': Sale.objects.order_by('-date')[:5],
        'low_stock_products': Product.objects.filter(stock_quantity__lte=models.F('minimum_stock'))[:5]
    }
    return render(request, 'core/dashboard.html', context)

class ProductListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Product
    template_name = 'core/product_list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Product
    template_name = 'core/product_form.html'
    fields = ['name', 'description', 'price', 'stock_quantity', 'minimum_stock',
              'category', 'animal_type', 'brand', 'weight', 'weight_unit',
              'expiration_date']
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Produto cadastrado com sucesso!')
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'core/product_form.html'
    fields = ['name', 'description', 'price', 'stock_quantity', 'minimum_stock',
              'category', 'animal_type', 'brand', 'weight', 'weight_unit',
              'expiration_date']
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'core/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Produto excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class CustomerListView(ListView):
    model = Customer
    template_name = 'core/customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'core/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'core/customer_form.html'
    fields = ['name', 'email', 'phone', 'address', 'has_pets', 'pet_notes']
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return super().form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    template_name = 'core/customer_form.html'
    fields = ['name', 'email', 'phone', 'address', 'has_pets', 'pet_notes']
    success_url = reverse_lazy('customer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'core/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class InventoryListView(ListView):
    model = InventoryMovement
    template_name = 'core/inventory_list.html'
    context_object_name = 'movements'

class InventoryMovementCreateView(CreateView):
    model = InventoryMovement
    template_name = 'core/inventory_movement_form.html'
    fields = ['product', 'quantity', 'movement_type', 'notes', 'batch_number', 'supplier']
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        messages.success(self.request, 'Movimentação de estoque registrada com sucesso!')
        return super().form_valid(form)

class SaleListView(ListView):
    model = Sale
    template_name = 'core/sale_list.html'
    context_object_name = 'sales'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'core/sale_detail.html'
    context_object_name = 'sale'

class SaleCreateView(CreateView):
    model = Sale
    template_name = 'core/sale_form.html'
    fields = ['customer', 'payment_method', 'notes']
    success_url = reverse_lazy('sale_list')

    def form_valid(self, form):
        messages.success(self.request, 'Venda registrada com sucesso!')
        return super().form_valid(form)
