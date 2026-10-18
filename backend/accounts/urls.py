from django.urls import path

from .views import (
    ManagerDashboardView,
    CashierDashboardView,
)

urlpatterns = [
    path(
        "manager/dashboard/",
        ManagerDashboardView.as_view()
    ),

    path(
        "cashier/dashboard/",
        CashierDashboardView.as_view()
    ),
]