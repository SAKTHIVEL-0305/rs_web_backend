from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Order, Quote, Invoice, ContactMessage


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering      = ('-date_joined',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ('pk', 'user', 'order_type', 'design_name', 'size_display', 'status', 'urgent', 'date_needed', 'created_at')
    list_filter    = ('order_type', 'status', 'urgent')
    search_fields  = ('design_name', 'user__email', 'po_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {'fields': ('user', 'order_type', 'status', 'design_name', 'po_number', 'urgent', 'date_needed')}),
        ('Dimensions', {'fields': ('width_mm', 'height_mm', 'size_unit')}),
        ('Digitizing', {'fields': ('format', 'fabric', 'colors', 'placement', 'instructions')}),
        ('Patches', {'fields': ('patch_type', 'backing', 'border_type', 'quantity', 'embroidery_pct', 'thread_color')}),
        ('Vector', {'fields': ('vector_format', 'background')}),
        ('Files', {'fields': ('design_file', 'reference_file')}),
        ('Pricing', {'fields': ('price',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display   = ('pk', 'user', 'quote_type', 'design_name', 'size_display', 'status', 'quoted_price', 'urgent', 'date_needed', 'created_at')
    list_filter    = ('quote_type', 'status', 'urgent')
    search_fields  = ('design_name', 'user__email', 'po_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic', {'fields': ('user', 'quote_type', 'status', 'design_name', 'po_number', 'urgent', 'date_needed')}),
        ('Dimensions', {'fields': ('width_mm', 'height_mm', 'size_unit')}),
        ('Digitizing', {'fields': ('fabric', 'colors', 'placement', 'description')}),
        ('Patches', {'fields': ('patch_type', 'backing', 'border_type', 'quantity', 'embroidery_pct', 'thread_color')}),
        ('Vector', {'fields': ('vector_format', 'background')}),
        ('Files', {'fields': ('design_file',)}),
        ('Pricing', {'fields': ('quoted_price', 'admin_notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display  = ('invoice_number', 'user', 'order', 'amount', 'status', 'due_date', 'created_at')
    list_filter   = ('status',)
    search_fields = ('invoice_number', 'user__email')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'service', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
