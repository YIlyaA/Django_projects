# Django_projects
### Interesting Django Project Ideas for All Levels — Beginners to Advanced Level

<details>
<summary><h2><bold>1. To-Do List Application:</bold></h2></summary>

   Simple to-do list app where users can add, edit, and delete tasks. User email authentication allow each user to manage their own task list.

   https://github.com/user-attachments/assets/1a31712b-cb53-4a63-a1c1-38e082b7a7c2

  1. **Install Dependencies**:
   Use Pipenv to manage your environment:
   ```bash
   pipenv shell
   pipenv install
  ```
  2. **Configure Environment Variables**: Create a .env file in the root of your project and fill it with the following example content:
  ```
  SECRET_KEY=django-insecure-1&cf6w&mwq7@-h^@jx=mbn)xwj=jw^@l!^j6!9&bw6%=$5!&lz
  DEBUG=True
  ALLOWED_HOSTS=localhost,127.0.0.1
  DATABASE_URL=db.sqlite3
  ```
  3. **Apply Migrations**: Run the following commands to apply database migrations:
  ```
  python manage.py migrate
  ```
  4. **Create a Superuser**: Create a superuser to access the Django admin panel:
  ```
  python manage.py createsuperuser
  ```
  4. **Run the Development Server**: Start the development server:
  ```
  python manage.py runserver
  ```
  5. You can now access the application at `http://127.0.0.1:8000/login/`
</details>

<details>
   <summary><h2><bold>2. Blog Platform</bold></h2></summary>
   
   A basic blogging platform where users can create, edit, and delete posts. Include features like commenting, tagging, and categorization to organize posts effectively.   
   
   [Untitled Video November 7, 2024 5_35 PM.webm](https://github.com/user-attachments/assets/8b108d35-be64-479d-abad-1112bd0ecd24)

   1. **Install Dependencies**:
   Use Pipenv to manage your environment:
   ```bash
   pipenv shell
   pipenv install
  ```
  2. **Configure Environment Variables**: Create a .env file in the root of your project and fill it with the following example content:
  ```
  SECRET_KEY=django-insecure-1&cf6w&mwq7@-h^@jx=mbn)xwj=jw^@l!^j6!9&bw6%=$5!&lz
  DEBUG=True
  ALLOWED_HOSTS=localhost,127.0.0.1
  DATABASE_URL=db.sqlite3
  ```
  3. **Apply Migrations**: Run the following commands to apply database migrations:
  ```
  python manage.py migrate
  ```
  4. **Create a Superuser**: Create a superuser to access the Django admin panel:
  ```
  python manage.py createsuperuser
  ```
  4. **Run the Development Server**: Start the development server:
  ```
  python manage.py runserver
  ```
  5. You can now access the application at `http://127.0.0.1:8000/account/login/`
</details>
