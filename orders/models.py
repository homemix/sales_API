from django.db import models
from customers.models import Customer


class Order(models.Model):
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order {self.id} for {self.item} by {self.customer.name}"
