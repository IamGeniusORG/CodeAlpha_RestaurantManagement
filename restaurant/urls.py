from django.urls import path
from . import views

urlpatterns = [
    path('', views.DigitalMenuView.as_view(), name='menu'),
    path('reserve/', views.ReserveTableView.as_view(), name='reserve'),
    path('order/', views.PlaceOrderView.as_view(), name='order'),
    
    # Staff Routes
    path('staff/dashboard/', views.StaffDashboardView.as_view(), name='staff_dashboard'),
    path('staff/orders/', views.StaffOrdersView.as_view(), name='staff_orders'),
    path('staff/orders/<int:pk>/update/', views.UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('staff/inventory/', views.StaffInventoryView.as_view(), name='staff_inventory'),
]
