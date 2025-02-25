## **🛠️ Step 1: Setup Project Structure**
Create a new project folder:
```
mkdir external-data-model && cd external-data-model
python -m venv <virtual-environment-name>
<virtual-environment-name>/Scripts/activate.bat //In CMD
<virtual-environment-name>/Scripts/Activate.ps1 //In Powershel
```

Inside, create the following structure:
```
external-data-model/
├── src/
│   ├── external_data_model/       # Reusable SQLAlchemy model package
│   │   ├── models/                     # Database models
│   │   │   ├── __init__.py
│   │   │   ├── base.py                 # Declarative Base
│   │   │   ├── electricity.py                 # Add external-data-model classes here
            ...
│   │   ├── db_connector.py             # Database connection logic
│   │   ├── __init__.py
│
├── tests/
│   ├── test_user.py                # Unit tests for User model
│   ├── conftest.py                 # Pytest fixtures
│   ├── requirements.txt
│
├── pyproject.toml                   # PEP 621 packaging standard
├── README.md                        # Project documentation
├── .gitignore                        # Ignore unwanted files
├── docker-compose.yml                # Local PostgreSQL DB for development

```

## **📌 Step 2: Install Dependencies**
We’ll use `SQLAlchemy` for ORM and `Alembic` for migrations.
```
pip install sqlalchemy alembic psycopg2-binary python-dotenv pre-commit
cd src/external_data_model/
alembic init migrations
```
Now structure will be like below and add directory migration and alembic.ini under src/hh2e_external_data_model/
```
external-data-model/
├── src/
│   ├── external_data_model/

  ...

│   │   ├── migrations/                # Alembic migration files
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   ├── versions/
│   │   ├── alembic.ini

  ...

```

## **📌 Step 3: Set Up Database Connection**

Update `db_connector.py` to configure the database connection.

### **2️⃣ Configure Alembic**
Edit `alembic.ini`, and comment this line:
```ini
sqlalchemy.url =
```
👉 Instead, we will use enviornment variable.

```
# For windows
$env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/localdb"
# For Linux
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/mydb"
```
---

## **📌 Step 4: Configure Alembic to Use SQLAlchemy Models**

Edit `migrations/env.py` and add following lines where appropriate

```python
...
# Access command-line options
cmd_opts = context.get_x_argument(as_dictionary=True)

if cmd_opts.get("env") == "production":
    prod_url = os.getenv("PROD_URL")
    if prod_url:
        config.set_main_option("sqlalchemy.url", prod_url)
    else:
        raise ValueError("PROD_URL environment variable not set")
else:
    local_url = os.getenv("LOCAL_URL")
    if local_url:
        config.set_main_option("sqlalchemy.url", local_url)
    else:
        raise ValueError("LOCAL_URL environment variable not set")

```

## **📌 Step 5: Create and Apply Migrations**

1️⃣ Generate migration script:
```bash
alembic revision --autogenerate -m "Create external_data table"
```
2️⃣ Apply migration to the database:
```bash
alembic upgrade head
```
🎉 Your `tables` are now created! verify with below commands

```
# psql -U postgres
# psql -U postgres -d localdb -c "select table_name from information_schema.tables where table_schema='public' ;"
```
---

Following steps will be perform during development
## **📌 Step 6: Deploy with Docker Compose**

Create `docker-compose.yml` for PostgreSQL:
```yaml
version: "3.8"
services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
  app:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://user:password@db/mydb
```

Run everything with:
```bash
docker-compose up --build -d
```
✔️ **Your database is now running in Docker.** 🚀

Perform step 5

---

pre-commit run --all-files
