from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from restaurant.models import Table, Reservation, InventoryItem, MenuItem, RecipeRequirement, Order
from restaurant.services import ReservationService, OrderService

class ReservationServiceTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_number=1, capacity=4)
        self.base_time = timezone.now() + timedelta(days=1)
        
        # Create an existing reservation
        Reservation.objects.create(
            customer_name="John Doe",
            contact="1234567890",
            table=self.table,
            reservation_time=self.base_time,
            guest_count=2,
            status="Confirmed"
        )

    def test_availability_conflict(self):
        # Exact same time
        is_available = ReservationService.check_availability(self.table, self.base_time)
        self.assertFalse(is_available)

        # 1 hour later (still conflicts if duration is 2 hours)
        is_available = ReservationService.check_availability(self.table, self.base_time + timedelta(hours=1))
        self.assertFalse(is_available)

    def test_availability_no_conflict(self):
        # 3 hours later (no conflict)
        is_available = ReservationService.check_availability(self.table, self.base_time + timedelta(hours=3))
        self.assertTrue(is_available)

class OrderServiceTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_number=2, capacity=2)
        
        self.cheese = InventoryItem.objects.create(
            name="Cheese", quantity=Decimal('10.00'), unit="kg", low_stock_threshold=Decimal('2.00')
        )
        self.dough = InventoryItem.objects.create(
            name="Dough", quantity=Decimal('20.00'), unit="kg", low_stock_threshold=Decimal('5.00')
        )

        self.pizza = MenuItem.objects.create(
            name="Pizza", description="Cheese Pizza", price=Decimal('12.50'), is_available=True
        )

        RecipeRequirement.objects.create(
            menu_item=self.pizza, inventory_item=self.cheese, quantity_required=Decimal('0.50')
        )
        RecipeRequirement.objects.create(
            menu_item=self.pizza, inventory_item=self.dough, quantity_required=Decimal('1.00')
        )

    def test_process_order_inventory_deduction(self):
        # Order 2 pizzas
        items_data = {self.pizza.id: 2}
        order = OrderService.process_order(self.table.id, items_data)

        self.assertEqual(order.total_amount, Decimal('25.00'))
        self.assertEqual(order.table, self.table)

        # Check inventory deductions
        self.cheese.refresh_from_db()
        self.dough.refresh_from_db()

        self.assertEqual(self.cheese.quantity, Decimal('9.00')) # 10 - (0.5 * 2)
        self.assertEqual(self.dough.quantity, Decimal('18.00')) # 20 - (1.0 * 2)
