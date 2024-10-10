# КГТС Бот Поддержки

## Описание

Это официальный бот поддержки КГТС, созданный делевером. Бот предназначен для автоматизации ответов на часто задаваемые вопросы, предоставления информации о услугах и поддержки пользователей в реальном времени.

## Версия

**Версия:** 2.1

## Технологии

- Язык программирования: Python
- Библиотеки: [aiogram](https://github.com/aiogram/aiogram) для работы с Telegram API.

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/IMDelewer/kgts.git
   cd kgts
   ```

2. **Создайте виртуальное окружение и активируйте его:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте конфигурацию:**

   Откройте файл `config.py` и добавьте ваш токен и URL базы данных:

   ```python
   class Config:
       admins = [
           "5665997196"
       ]
       
       token = "ваш_токен_бота"
       db_name = 'kgts'
       url = "ваш_url_базы_данных"
       version = "2.1"
       github = "https://github.com/IMDelewer/kgts"
   ```

## Запуск

Чтобы запустить бота, выполните следующую команду:

```bash
python3 .
```

## Функциональность

- Ответы на часто задаваемые вопросы.
- Поддержка пользователей в реальном времени.
- Информация о новых услугах и обновлениях.

## Использование

После запуска бота вы можете начать с ним взаимодействовать в Telegram. Просто найдите бота по его имени и отправьте любое сообщение, чтобы получить ответ.

## Поддержка

Если у вас возникли вопросы или проблемы, вы можете связаться с нами через:

- Telegram: [@imdelewer](https://t.me/imdelewer)
- Электронную почту: <delewer@asphr.xyz>

## Лицензия

Этот проект лицензирован под MIT License. Подробности можно найти в файле [LICENSE](LICENSE).

## Вклад

Если вы хотите внести вклад в проект, пожалуйста, создайте форк, внесите изменения и отправьте пулл-реквест.

---

Спасибо за использование нашего бота! Мы ценим ваше мнение и готовы помочь вам в любое время.
