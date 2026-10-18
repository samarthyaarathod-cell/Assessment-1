# Section B Django CRUD

This is the MenuItem CRUD site with a responsive custom frontend and a separate Jazzmin admin panel at `/panel/`. The old `/admin/` path redirects to the panel. Its CSS and JavaScript are served locally, so layout and navigation still work without Bootstrap/CDN access. Bootstrap 5 CDN is also loaded as required by the brief.

## Run locally
1. `py -m venv .venv`
2. Activate it: `\.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. `py manage.py migrate`
5. `py manage.py createsuperuser`
6. `py manage.py runserver`

Open `/` or `/menu/`. Sign in to `/panel/` with your superuser account, then add a Restaurant at `/panel/menuapp/restaurant/add/`. The MenuItem form needs at least one Restaurant, and now explains this when the list is empty. Then add menu items from `/menu/add/`. Staff can open the separate dashboard at `/panel/`.

Create, update, and delete are login-protected; menu listing is public. For assessment evidence, capture the menu list, create, edit, and delete confirmation pages after adding sample data.


