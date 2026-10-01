from django.contrib import admin
from .models import Table, Reservation, InventoryItem, MenuItem, RecipeRequirement, Order, OrderItem

class RecipeRequirementInline(admin.TabularInline):
    model = RecipeRequirement
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    search_fields = ('name',)
    list_filter = ('is_available',)
    inlines = [RecipeRequirementInline]

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_active')
    search_fields = ('table_number',)
    list_filter = ('is_active',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'table', 'reservation_time', 'guest_count', 'status')
    search_fields = ('customer_name', 'contact')
    list_filter = ('status', 'reservation_time')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'low_stock_threshold', 'is_low_stock')
    search_fields = ('name',)
    list_filter = ('unit',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(RecipeRequirement)
class RecipeRequirementAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'inventory_item', 'quantity_required')
    search_fields = ('menu_item__name', 'inventory_item__name')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity')
