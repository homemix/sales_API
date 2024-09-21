import requests
from rest_framework import viewsets, status
from rest_framework.response import Response

from customers.models import Customer
from .models import Order
from .serializers import OrderSerializer
from services.sending_sms import SendSMS


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Call the original create method to save the order
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # After creating the order, send a notification to an external API
        order_data = serializer.data  # The saved order data

        customer = Customer.objects.get(id=order_data['customer'])
        phone_number = customer.phone_number

        message = f'''
        Hello {customer.name} , Your Order #{order_data['id']} has {order_data['item']}
        and Cost is {order_data['amount']},
        Thank for shopping with us.
                '''

        sms_service = SendSMS(message=message, recipient=phone_number)
        sms_service.send_message_sync()
        if sms_service.success is False:
            headers = self.get_success_headers(serializer.data)
            return Response({'error':'SMS API credentials are wrong'}, status=status.HTTP_503_SERVICE_UNAVAILABLE, headers=headers)

        # Return the original response with the created order
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
