# EduOS — Part 1 Foundation

Part 1 establishes the production-oriented K-12 ERP foundation.

## Included in this drop

- Existing EduOS dashboard, student, guardian, teacher, academics, attendance and leave modules preserved.
- Dashboard test suite corrected so activity-log tests are actual Django test methods rather than nested functions.
- Environment-driven Django secret key, DEBUG and ALLOWED_HOSTS.
- Production security cookie/header defaults.
- `.env.example` for local/Render configuration.
- Accessible skip navigation.
- School context in the application shell.
- Ctrl/Cmd+K global navigation search.
- Responsive-friendly error pages for 403/404/500.
- Existing migrations preserved, including the dashboard migration already present in the supplied ZIP.

## Before deploying

Set these Render environment variables:

- `DEBUG=False`
- `DJANGO_SECRET_KEY=<strong-random-secret>`
- `ALLOWED_HOSTS=eduos-sulp.onrender.com`

Do not commit a real production secret key.

## Next parts

Part 2: daily school operations and role-specific workflows.

Part 3: fees/finance + examinations/results.

Part 4: library/transport/communications/reports + final production hardening.
