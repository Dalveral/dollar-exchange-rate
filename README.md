# dollar-exchange-rate

## Установка окружения
```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## Применение миграций
```bash
python manage.py migrate
```

## Запуск приложения
```bash
python manage.py runserver
```

## Получить актуальный курс
```bash
http://127.0.0.1:8000/get-current-usd/
```