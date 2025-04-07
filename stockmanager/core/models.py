from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Pet Food'),
        ('SUPPLIES', 'Pet Supplies'),
        ('ACCESSORIES', 'Pet Accessories'),
        ('MEDICINE', 'Pet Medicine'),
        ('HYGIENE', 'Pet Hygiene Products')
    ]
    
    ANIMAL_TYPE_CHOICES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('FISH', 'Fish'),
        ('SMALL_ANIMAL', 'Small Animal'),
        ('REPTILE', 'Reptile'),
        ('ALL', 'All Animals')
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='SUPPLIES')
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPE_CHOICES, default='ALL')
    brand = models.CharField(max_length=100, default='Generic')
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    weight_unit = models.CharField(max_length=10, default='kg')
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.brand} ({self.get_animal_type_display()})'

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    has_pets = models.BooleanField(default=True)
    pet_notes = models.TextField(blank=True, help_text='Notes about customer\'s pets')
    loyalty_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InventoryMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    supplier = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if self.movement_type == 'IN':
            self.product.stock_quantity += self.quantity
        else:
            self.product.stock_quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('CREDIT', 'Credit Card'),
        ('DEBIT', 'Debit Card'),
        ('PIX', 'PIX'),
        ('TRANSFER', 'Bank Transfer')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    notes = models.TextField(blank=True)
    loyalty_points_earned = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.loyalty_points_earned = int(self.total_amount)
            self.customer.loyalty_points += self.loyalty_points_earned
            self.customer.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Sale {self.id} - {self.customer.name}'

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
