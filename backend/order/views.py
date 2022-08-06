import stripe
from django.conf import settings
from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer


class Checkout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            paid_amount = sum(
                item.get("quantity") * item.get("product").price
                for item in serializer.validated_data["items"]
            )

            try:
                charge = stripe.Charge.create(
                    amount=int(paid_amount * 100),
                    currency="USD",
                    description="Charge from Djackets",
                    source=serializer.validated_data["stripe_token"],
                )
                serializer.save(user=request.user, paid_amount=paid_amount)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
