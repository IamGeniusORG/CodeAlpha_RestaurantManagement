from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta
from .models import Reservation, Table, Order, OrderItem, MenuItem, InventoryItem

class ReservationService:
    @staticmethod
    def check_availability(table, reservation_time, duration_hours=2):
        """
        Checks if a table is available at the given time.
        Assumes each reservation lasts for `duration_hours`.
        """
        end_time = reservation_time + timedelta(hours=duration_hours)
        start_time = reservation_time - timedelta(hours=duration_hours)

        conflicting_reservations = Reservation.objects.filter(
            table=table,
            reservation_time__lt=end_time,
            reservation_time__gt=start_time,
            status__in=['Pending', 'Confirmed']
        )
        
        return not conflicting_reservations.exists()

class OrderService:
    @staticmethod
    @transaction.atomic
    def process_order(table_id, items_data):
        """
        Processes an order:
        - Creates the Order and OrderItems.
        - Calculates total amount.
        - Deducts inventory based on RecipeRequirements.
        
        items_data is a dictionary mapping menu_item_id to quantity.
        """
        table = None
        if table_id:
            table = Table.objects.get(id=table_id)
            
        order = Order.objects.create(table=table, status='Pending')
        total_amount = 0
        
        for menu_item_id, quantity in items_data.items():
            if quantity <= 0:
                continue
                
            menu_item = MenuItem.objects.get(id=menu_item_id)
            
            # Create OrderItem
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )
            
            total_amount += menu_item.price * quantity
            
            # Deduct inventory
            for requirement in menu_item.recipe_requirements.all():
                inventory_item = requirement.inventory_item
                required_quantity = requirement.quantity_required * quantity
                
                # We could raise an error if insufficient stock, but usually
                # restaurants let it go negative to track missed counts.
                # Here we just deduct it.
                inventory_item.quantity -= required_quantity
                inventory_item.save()
                
        order.total_amount = total_amount
        order.save()
        
        return order
