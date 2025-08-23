# Django + Docker + ECS Example

## Local Development

1. Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```
   Visit http://localhost:8000

2. To run migrations:
   ```sh
   docker-compose run web python manage.py migrate
   ```

## ECS Deployment
- Set environment variables for DB and secret key in your ECS task definition.
- Use `testproject/settings_ecs.py` for ECS-specific settings (set `DJANGO_SETTINGS_MODULE=testproject.settings_ecs`).
- Use a production-ready database (e.g., RDS/PostgreSQL).

## Environment Variables
See `.env` for local and ECS variable examples.

---

This project is a minimal Django app containerized for easy deployment to AWS ECS.
