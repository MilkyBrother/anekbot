ANEKBOT - телеграм бот, который выдаёт уникальный анекдот для каждого пользователя.
Бот автоматически парсит анекдоты из различных источников, складывает их в базу данных и предоставляет их по запросу.
Также бот ведёт учёт выданных анекдотов каждому пользователю для гарантии выдачи анекдотов без повторов.


**Инструкция по запуску проекта:**

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/MilkyBrother/anekbot.git
   cd anekbot
   ```

2. **Установка зависимостей:**
   Убедитесь, что у вас установлен Python 3. Затем установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка переменных окружения:**
   Создайте файл `.env` в корневой директории проекта и добавьте в него ваш Telegram API токен:
   ```
   TELEGRAM_API_TOKEN=your_telegram_api_token
   ```

4. **Запуск бота:**
   ```bash
   python anekbot.py
   ```

После выполнения этих шагов бот будет готов к работе и сможет отправлять анекдоты пользователям в Telegram. 
