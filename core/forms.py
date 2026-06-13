from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Order, Quote


class RegisterForm(forms.ModelForm):
    first_name       = forms.CharField(max_length=150, min_length=2)
    last_name        = forms.CharField(max_length=150, min_length=1)
    email            = forms.EmailField()
    phone            = forms.CharField(max_length=15)
    password         = forms.CharField(widget=forms.PasswordInput, min_length=5)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    terms            = forms.BooleanField()

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].replace(' ', '')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone must be exactly 10 digits.")
        return phone

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password', '')
        cpw = cleaned.get('confirm_password', '')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError("Passwords do not match.")
        import re
        if pw and len(pw) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        if pw and not re.search(r'\d', pw):
            raise forms.ValidationError("Password must contain at least one number.")
        if pw and not re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', pw):
            raise forms.ValidationError("Password must contain at least one special character.")
        return cleaned

    def save(self, commit=True):
        user          = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email    = self.cleaned_data['email']
        user.phone    = self.cleaned_data['phone']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data.get('username', '').lower().strip()


# ── ORDER FORMS ───────────────────────────────────────────────────────────────

class OrderDigitizingForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = [
            'design_name', 'po_number',
            'width_mm', 'height_mm', 'size_unit',
            'colors', 'format', 'fabric', 'placement',
            'instructions', 'urgent', 'date_needed',
            'design_file', 'reference_file',
        ]
        widgets = {
            'urgent':      forms.CheckboxInput(),
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False
        self.fields['design_name'].required = True


class OrderPatchesForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = [
            'design_name', 'po_number',
            'width_mm', 'height_mm', 'size_unit',
            'colors', 'patch_type', 'backing', 'border_type',
            'quantity', 'embroidery_pct', 'thread_color',
            'instructions', 'urgent', 'date_needed',
            'design_file', 'reference_file',
        ]
        widgets = {
            'urgent':      forms.CheckboxInput(),
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False
        self.fields['design_name'].required = True


class OrderVectorForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = [
            'design_name', 'po_number',
            'vector_format', 'background', 'colors',
            'instructions', 'urgent', 'date_needed',
            'design_file',
        ]
        widgets = {
            'urgent':      forms.CheckboxInput(),
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False
        self.fields['design_name'].required = True


# ── QUOTE FORMS ───────────────────────────────────────────────────────────────

class QuoteDigitizingForm(forms.ModelForm):
    class Meta:
        model  = Quote
        fields = [
            'design_name', 'po_number',
            'width_mm', 'height_mm', 'size_unit',
            'colors', 'fabric', 'placement',
            'description', 'urgent', 'date_needed',
            'design_file',
        ]
        widgets = {
            'urgent':      forms.CheckboxInput(),
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False
        self.fields['design_name'].required = True


class QuotePatchesForm(forms.ModelForm):
    class Meta:
        model  = Quote
        fields = [
            'design_name', 'po_number',
            'width_mm', 'height_mm', 'size_unit',
            'colors', 'patch_type', 'backing', 'border_type',
            'quantity', 'embroidery_pct', 'thread_color',
            'description', 'urgent', 'date_needed',
            'design_file',
        ]
        widgets = {
            'urgent':      forms.CheckboxInput(),
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False
        self.fields['design_name'].required = True


class QuoteVectorForm(forms.ModelForm):
    class Meta:
        model  = Quote
        fields = [
            'design_name', 'po_number',
            'vector_format', 'background', 'colors',
            'description', 'urgent', 'date_needed',
            'design_file',
        ]
        widgets = {
            'urgent':      forms.CheckboxInput(),
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False
        self.fields['design_name'].required = True


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'phone']
