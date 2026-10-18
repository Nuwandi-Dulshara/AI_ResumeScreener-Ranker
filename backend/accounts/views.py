from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import HasAllowedRole


class ManagerDashboardView(APIView):

    permission_classes = [HasAllowedRole]

    allowed_roles = ["Admin", "Manager"]

    def get(self, request):

        return Response({
            "message": "Welcome to Manager Dashboard"
        })


class CashierDashboardView(APIView):

    permission_classes = [HasAllowedRole]

    allowed_roles = ["Admin", "Manager", "Cashier"]

    def get(self, request):

        return Response({
            "message": "Welcome to Cashier Dashboard"
        })