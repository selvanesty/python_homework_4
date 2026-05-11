import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError

# Дані для підключення з docker-compose.yml
DB_USER = 'user'
DB_PASSWORD = 'user_password'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'my_database'

# Формуємо URL для SQLAlchemy
engine_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(engine_url)

max_retries = 10
retry_delay = 10

print("Спроба підключення до бази даних...")

# Retry-логіка
for attempt in range(1, max_retries + 1):
    try:
        # Намагаємося встановити з'єднання
        with engine.connect() as connection:
            print(f"Успішне підключення! (Спроба {attempt})")

            # Зчитуємо дані
            query = "SELECT * FROM titanic"
            df = pd.read_sql(query, connection)

            print(f"\nЗавантажено рядків: {df.shape[0]}, колонок: {df.shape[1]}")
            print(df.head())
            break  # Якщо підключення успішне, виходимо з циклу

    # ТЕПЕР МИ ЛОВИМО ОБИДВІ ПОМИЛКИ
    except (OperationalError, ProgrammingError):
        print(f"База ще не готова (Спроба {attempt}/{max_retries}). Очікування {retry_delay} секунд...")
        time.sleep(retry_delay)
else:
    print("\nНе вдалося підключитися до бази даних після 10 спроб.")