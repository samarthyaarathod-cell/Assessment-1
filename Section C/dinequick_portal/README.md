# Section C — DineQuick ordering portal

## Run locally
1. `py -m venv .venv` and activate it.
2. `pip install -r requirements.txt`
3. `py manage.py makemigrations orders` then `py manage.py migrate`
4. `py manage.py createsuperuser`
5. `py manage.py runserver`
6. At `/panel/`, add restaurants and menu items. The Jazzmin-powered admin panel is separate from the customer portal. Register at `/register/`, verify the email OTP, then use `/accounts/login/` to request a fresh OTP and place orders.

Gmail SMTP is configured through the local `.env` file (not source code); the app sends sign-in codes and order confirmations from the configured sender. Keep `.env` private and exclude it from any ZIP or submission. `.env.example` lists the required variable names. OTP codes are 6 digits, expire after 5 minutes, and are limited to five verification attempts with a resend cooldown.

Order totals use `Decimal` and are calculated before saving. The append-only `orders_log.txt` write is wrapped in exception handling and always closes the file. For deployment, replace the development secret/debug settings, configure production storage, and use HTTPS.
