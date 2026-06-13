# RS Digitizing — Django Backend

## Project Structure
```
rsdigitizing/
├── core/
│   ├── models.py      # User, Order, Quote, Invoice
│   ├── views.py       # All views (index, auth, dashboard, orders, quotes, profile)
│   ├── urls.py        # URL routing
│   ├── forms.py       # RegisterForm, LoginForm, Order/Quote/Profile forms
│   ├── admin.py       # Django admin (full CRUD for admin)
│   └── migrations/
├── templates/
│   ├── index.html     # Homepage (your index.html with Django tags)
│   ├── auth.html      # Login + Register (your auth.html with Django forms)
│   └── dashboard.html # Dashboard (your dashboard.html with live DB data)
├── rsdigitizing/
│   ├── settings.py
│   └── urls.py
├── media/             # Uploaded files (designs, references)
├── db.sqlite3         # SQLite database
└── README.md
```

## Setup

```bash
pip install django pillow

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## URL Routes
| URL | View | Description |
|-----|------|-------------|
| `/` | index | Homepage |
| `/auth/` | auth_view | Login + Register |
| `/logout/` | logout_view | Logout |
| `/dashboard/` | dashboard | Customer dashboard |
| `/dashboard/place-order/` | place_order | POST: submit new order |
| `/dashboard/place-quote/` | place_quote | POST: submit new quote |
| `/dashboard/update-profile/` | update_profile | POST: update profile |
| `/admin/` | Django admin | Full admin panel |

## Admin Credentials (default)
- Email: admin@rsdigitizing.com
- Password: Admin@123

## Models
- **User** — Extended Django user with `phone` field
- **Order** — Digitizing / Patches / Vector orders with file uploads
- **Quote** — Quote requests with all fields
- **Invoice** — Uninvoiced / Unpaid / Paid invoices linked to orders

## Features
- ✅ Login & Register with server-side validation
- ✅ Session-based authentication
- ✅ Dashboard with live stats from DB
- ✅ Order Records table — dynamic
- ✅ Quote Records table — dynamic
- ✅ Billing tables (Uninvoiced / Unpaid / Paid) — dynamic
- ✅ Place Order (Digitizing / Patches / Vector) — saves to DB
- ✅ Place Quote (Digitizing / Patches / Vector) — saves to DB
- ✅ Profile update — saves to DB
- ✅ File uploads for design files
- ✅ Django Admin panel — manage orders, quotes, invoices, users
- ✅ Flash messages for success/error feedback
