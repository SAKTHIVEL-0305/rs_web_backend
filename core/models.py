from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class Order(models.Model):
    ORDER_TYPES = [
        ('digitizing', 'Embroidery Digitizing'),
        ('patches', 'Patches'),
        ('vector', 'Vector Art'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]
    FORMAT_CHOICES = [
        ('DST', 'DST'), ('PES', 'PES'), ('EXP', 'EXP'),
        ('JEF', 'JEF'), ('VP3', 'VP3'), ('EMB', 'EMB'), ('XXX', 'XXX'), ('OTHER', 'Other'),
    ]
    UNIT_CHOICES = [
        ('in', 'Inches'),
        ('cm', 'CM'),
        ('mm', 'MM'),
    ]

    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_type      = models.CharField(max_length=20, choices=ORDER_TYPES)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    design_name     = models.CharField(max_length=200)
    po_number       = models.CharField(max_length=100, blank=True)
    width_mm        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height_mm       = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    size_unit       = models.CharField(max_length=5, choices=UNIT_CHOICES, default='in', blank=True)
    format          = models.CharField(max_length=10, choices=FORMAT_CHOICES, blank=True)
    fabric          = models.CharField(max_length=100, blank=True)
    colors          = models.PositiveIntegerField(null=True, blank=True)
    placement       = models.CharField(max_length=100, blank=True)
    instructions    = models.TextField(blank=True)
    urgent          = models.BooleanField(default=False)
    date_needed     = models.DateField(null=True, blank=True)
    design_file     = models.FileField(upload_to='orders/designs/', null=True, blank=True)
    reference_file  = models.FileField(upload_to='orders/references/', null=True, blank=True)
    # Patches-specific
    patch_type      = models.CharField(max_length=100, blank=True)
    quantity        = models.PositiveIntegerField(null=True, blank=True)
    border_type     = models.CharField(max_length=100, blank=True)
    backing         = models.CharField(max_length=100, blank=True)
    thread_color    = models.TextField(blank=True)
    embroidery_pct  = models.CharField(max_length=10, blank=True)
    # Vector-specific
    vector_format   = models.CharField(max_length=50, blank=True)
    background      = models.CharField(max_length=50, blank=True)
    # Pricing
    price           = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def size_display(self):
        if self.width_mm and self.height_mm:
            unit = self.size_unit or 'in'
            return f"{self.width_mm} × {self.height_mm} {unit}"
        return "—"

    def __str__(self):
        return f"Order #{self.pk} — {self.design_name}"


class Quote(models.Model):
    QUOTE_TYPES = [
        ('digitizing', 'Embroidery Digitizing'),
        ('patches', 'Patches'),
        ('vector', 'Vector Art'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('quoted', 'Quoted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    UNIT_CHOICES = [
        ('in', 'Inches'),
        ('cm', 'CM'),
        ('mm', 'MM'),
    ]

    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')
    quote_type      = models.CharField(max_length=20, choices=QUOTE_TYPES)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    design_name     = models.CharField(max_length=200)
    po_number       = models.CharField(max_length=100, blank=True)
    width_mm        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height_mm       = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    size_unit       = models.CharField(max_length=5, choices=UNIT_CHOICES, default='in', blank=True)
    fabric          = models.CharField(max_length=100, blank=True)
    colors          = models.PositiveIntegerField(null=True, blank=True)
    placement       = models.CharField(max_length=100, blank=True)
    description     = models.TextField(blank=True)
    urgent          = models.BooleanField(default=False)
    date_needed     = models.DateField(null=True, blank=True)
    design_file     = models.FileField(upload_to='quotes/designs/', null=True, blank=True)
    # Patches-specific
    patch_type      = models.CharField(max_length=100, blank=True)
    quantity        = models.PositiveIntegerField(null=True, blank=True)
    border_type     = models.CharField(max_length=100, blank=True)
    backing         = models.CharField(max_length=100, blank=True)
    thread_color    = models.TextField(blank=True)
    embroidery_pct  = models.CharField(max_length=10, blank=True)
    # Vector-specific
    vector_format   = models.CharField(max_length=50, blank=True)
    background      = models.CharField(max_length=50, blank=True)
    # Admin
    quoted_price    = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    admin_notes     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def size_display(self):
        if self.width_mm and self.height_mm:
            unit = self.size_unit or 'in'
            return f"{self.width_mm} × {self.height_mm} {unit}"
        return "—"

    def __str__(self):
        return f"Quote #{self.pk} — {self.design_name}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('uninvoiced', 'Uninvoiced'),
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    order          = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uninvoiced')
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    description    = models.TextField(blank=True)
    due_date       = models.DateField(null=True, blank=True)
    paid_at        = models.DateTimeField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number} — Rs.{self.amount}"


class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ('Logo Digitizing', 'Logo Digitizing'),
        ('3D Puff Embroidery', '3D Puff Embroidery'),
        ('Cap Digitizing', 'Cap Digitizing'),
        ('Screen Printing', 'Screen Printing'),
        ('Vinyl Cutting / HTV', 'Vinyl Cutting / HTV'),
        ('Digital Printing & Stickers', 'Digital Printing & Stickers'),
        ('Corporate Uniforms', 'Corporate Uniforms'),
        ('Sports Uniforms', 'Sports Uniforms'),
        ('Custom Design Work', 'Custom Design Work'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=15)
    service    = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.service} ({self.email})"
