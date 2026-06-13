from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Order, Quote, Invoice, ContactMessage
from .forms import (
    RegisterForm, LoginForm,
    OrderDigitizingForm, OrderPatchesForm, OrderVectorForm,
    QuoteDigitizingForm, QuotePatchesForm, QuoteVectorForm,
    ProfileForm,
)


# ─── PUBLIC PAGES ─────────────────────────────────────────────────────────────

def index(request):
    return render(request, 'index.html', {'user': request.user})


# ─── AUTH ─────────────────────────────────────────────────────────────────────

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    login_form    = LoginForm()
    register_form = RegisterForm()
    panel         = 'login'
    errors        = {}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            panel    = 'login'
            email    = request.POST.get('username', '').strip().lower()
            password = request.POST.get('password', '')
            user     = authenticate(request, username=email, password=password)
            if user is None:
                try:
                    u    = User.objects.get(email=email)
                    user = authenticate(request, username=u.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                errors['login'] = 'Invalid email or password. Please try again.'

        elif action == 'register':
            panel         = 'register'
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
                return redirect('dashboard')
            else:
                err_list = []
                for field, errs in register_form.errors.items():
                    for e in errs:
                        err_list.append(e if field == '__all__' else str(e))
                errors['register'] = ' '.join(err_list)

    return render(request, 'auth.html', {
        'login_form':    login_form,
        'register_form': register_form,
        'panel':         panel,
        'errors':        errors,
    })


def contact_submit(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name',  '').strip()
        email      = request.POST.get('email',      '').strip()
        phone      = request.POST.get('phone',      '').replace(' ', '')
        service    = request.POST.get('service',    '').strip()
        message    = request.POST.get('message',    '').strip()

        errors = []
        if not first_name: errors.append('First name is required.')
        if not last_name:  errors.append('Last name is required.')
        if not email:      errors.append('Email is required.')
        if not phone.isdigit() or len(phone) != 10:
            errors.append('Phone must be exactly 10 digits.')
        if not service: errors.append('Please select a service.')
        if not message: errors.append('Project details are required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        ContactMessage.objects.create(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone, service=service, message=message,
        )
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': ['Invalid request.']}, status=400)


def logout_view(request):
    logout(request)
    return redirect('index')


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@login_required(login_url='/auth/')
def dashboard(request):
    user     = request.user
    orders   = Order.objects.filter(user=user)
    quotes   = Quote.objects.filter(user=user)
    invoices = Invoice.objects.filter(user=user)

    stats = {
        'total_orders':    orders.count(),
        'active_orders':   orders.filter(status__in=['new', 'in_progress']).count(),
        'total_quotes':    quotes.count(),
        'pending_quotes':  quotes.filter(status='pending').count(),
        'unpaid_invoices': invoices.filter(status='unpaid').count(),
    }

    context = {
        'stats':               stats,
        'recent_orders':       orders[:5],
        'recent_quotes':       quotes[:5],
        'orders':              orders,
        'quotes':              quotes,
        'invoices_uninvoiced': invoices.filter(status='uninvoiced'),
        'invoices_unpaid':     invoices.filter(status='unpaid'),
        'invoices_paid':       invoices.filter(status='paid'),
        'view':                request.GET.get('view', 'dashboard'),
        'order_digitizing_form': OrderDigitizingForm(),
        'order_patches_form':    OrderPatchesForm(),
        'order_vector_form':     OrderVectorForm(),
        'quote_digitizing_form': QuoteDigitizingForm(),
        'quote_patches_form':    QuotePatchesForm(),
        'quote_vector_form':     QuoteVectorForm(),
        'profile_form':          ProfileForm(instance=user),
    }
    return render(request, 'dashboard.html', context)


# ─── PLACE ORDER ─────────────────────────────────────────────────────────────

@login_required(login_url='/auth/')
def place_order(request):
    if request.method != 'POST':
        return redirect('dashboard')

    order_type = request.POST.get('order_type', 'digitizing')
    FORM_MAP   = {
        'digitizing': OrderDigitizingForm,
        'patches':    OrderPatchesForm,
        'vector':     OrderVectorForm,
    }
    FormClass = FORM_MAP.get(order_type, OrderDigitizingForm)

    # Merge size_unit into a single field for both height and width
    post_data = request.POST.copy()

    # The frontend sends height_unit / width_unit — store whichever is first as size_unit
    size_unit = post_data.get('height_unit') or post_data.get('width_unit') or 'in'
    post_data['size_unit'] = size_unit

    # urgent checkbox — frontend sends 'on' or nothing
    post_data['urgent'] = 'true' if post_data.get('urgent') == 'on' else 'false'

    form = FormClass(post_data, request.FILES)

    if form.is_valid():
        order            = form.save(commit=False)
        order.user       = request.user
        order.order_type = order_type
        order.size_unit  = size_unit
        order.urgent     = (post_data.get('urgent') == 'true')
        order.save()
        messages.success(request, f"✅ Order #{order.pk} placed successfully!")
    else:
        for field, errs in form.errors.items():
            for e in errs:
                messages.error(request, str(e))

    return redirect('/dashboard/?view=orders')


# ─── PLACE QUOTE ─────────────────────────────────────────────────────────────

@login_required(login_url='/auth/')
def place_quote(request):
    if request.method != 'POST':
        return redirect('dashboard')

    quote_type = request.POST.get('quote_type', 'digitizing')
    FORM_MAP   = {
        'digitizing': QuoteDigitizingForm,
        'patches':    QuotePatchesForm,
        'vector':     QuoteVectorForm,
    }
    FormClass = FORM_MAP.get(quote_type, QuoteDigitizingForm)

    post_data = request.POST.copy()
    size_unit = post_data.get('height_unit') or post_data.get('width_unit') or 'in'
    post_data['size_unit'] = size_unit
    post_data['urgent'] = 'true' if post_data.get('urgent') == 'on' else 'false'

    form = FormClass(post_data, request.FILES)

    if form.is_valid():
        quote            = form.save(commit=False)
        quote.user       = request.user
        quote.quote_type = quote_type
        quote.size_unit  = size_unit
        quote.urgent     = (post_data.get('urgent') == 'true')
        quote.save()
        messages.success(request, f"✅ Quote #{quote.pk} submitted successfully!")
    else:
        for field, errs in form.errors.items():
            for e in errs:
                messages.error(request, str(e))

    return redirect('/dashboard/?view=quotes')


# ─── PROFILE UPDATE ───────────────────────────────────────────────────────────

@login_required(login_url='/auth/')
def update_profile(request):
    if request.method != 'POST':
        return redirect('dashboard')

    form = ProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        user          = form.save(commit=False)
        user.username = user.email
        user.save()
        messages.success(request, "Profile updated successfully!")
    else:
        for field, errs in form.errors.items():
            for e in errs:
                messages.error(request, str(e))

    return redirect('/dashboard/?view=profile')
