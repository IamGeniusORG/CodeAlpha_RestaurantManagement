from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import MenuItem, Reservation, Table
from .forms import ReservationForm
from .services import OrderService

class DigitalMenuView(ListView):
    model = MenuItem
    template_name = 'public/menu.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        return MenuItem.objects.filter(is_available=True)

class ReserveTableView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'public/reserve.html'
    success_url = reverse_lazy('reserve')

    def form_valid(self, form):
        messages.success(self.request, "Your reservation has been placed successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your reservation. Please check the details below.")
        return super().form_invalid(form)

class PlaceOrderView(TemplateView):
    template_name = 'public/order.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.filter(is_active=True)
        context['menu_items'] = MenuItem.objects.filter(is_available=True)
        return context
    
    def post(self, request, *args, **kwargs):
        table_id = request.POST.get('table_id')
        items_data = {}
        
        # Extract item quantities from POST data
        for key, value in request.POST.items():
            if key.startswith('item_'):
                try:
                    menu_item_id = int(key.split('_')[1])
                    quantity = int(value)
                    if quantity > 0:
                        items_data[menu_item_id] = quantity
                except ValueError:
                    pass
        
        if not items_data:
            messages.error(request, "Please select at least one item to order.")
            return redirect('order')
            
        try:
            order = OrderService.process_order(table_id, items_data)
            messages.success(request, f"Order #{order.id} placed successfully! Total: ${order.total_amount}")
        except Exception as e:
            messages.error(request, f"There was an error processing your order: {str(e)}")
            
        return redirect('order')

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from .models import InventoryItem, Order

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class StaffDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'staff/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        # Active orders are Pending or Cooking
        context['active_orders'] = Order.objects.filter(status__in=['Pending', 'Cooking']).order_by('-created_at')
        # We can also get low stock items directly
        context['low_stock_items'] = [item for item in InventoryItem.objects.all() if item.is_low_stock]
        return context

class StaffOrdersView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'staff/active_orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return Order.objects.exclude(status='Completed').order_by('created_at')

class UpdateOrderStatusView(StaffRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    success_url = reverse_lazy('staff_orders')

    def form_valid(self, form):
        messages.success(self.request, f"Order #{self.object.id} status updated to {self.object.status}.")
        return super().form_valid(form)

class StaffInventoryView(StaffRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'staff/inventory.html'
    context_object_name = 'inventory_items'
