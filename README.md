# PhoneDeck — Станция для борьбы с информационной зависимостью

## Сайт
**http://109.73.206.169**

## Структура проекта

```
phonedeck/
├── app.py                 # Flask бэкенд (API + отдача React)
├── requirements.txt       # Python зависимости
├── Procfile               # Конфиг запуска (gunicorn)
├── build.sh               # Скрипт сборки (pip + npm + build)
├── frontend/              # React приложение (исходники)
│   ├── src/
│   │   ├── pages/         # Страницы (Обзор, Рейтинг, Статистика, Бонусы, Станция, Контакты)
│   │   ├── components/    # Компоненты (UserTable, Pagination, Header, Aside, Footer)
│   │   └── routes/        # React Router
│   └── package.json
└── arduino/               # Скетчи для микроконтроллеров
    ├── Arduino_230225/    # Arduino Uno — концевики, дисплеи, RTC
    ├── NodeMCU_updated/   # ESP8266 — WiFi + POST на сервер
    ├── ESP32S_POST.ino    # ESP32 — тестовый POST запрос
    ├── ESP32S_Sensors.ino # ESP32 — лазерные датчики
    ├── RTC_SetTime.ino    # Установка времени на часах RTC
    └── Display_SetAddress.ino # Установка адреса I2C дисплея
```

## Архитектура

```
[Телефон в слот] → [Концевик] → [Arduino Uno] → Serial → [ESP8266] → WiFi POST → [Сервер]
                                      ↓
                                [Дисплей ММ:СС]
```

- **Arduino Uno** — читает 6 концевиков, управляет дисплеями, считает время (RTC DS3231)
- **ESP8266 (NodeMCU Amica)** — принимает данные от Arduino по Serial, отправляет POST на сервер
- **Flask** — принимает данные (`POST /save`), отдаёт (`GET /get_data`), раздаёт React фронтенд
- **React** — отображает данные: таблицы пользователей, рейтинг, статистика, бонусы

## API

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST  | `/save`  | Сохранить данные устройства (JSON: name, model, charge, connection_time, disconnection_time) |
| GET   | `/get_data` | Получить все записи устройств |

## Хостинг

- **VPS**: Timeweb Cloud (Ubuntu 24.04, Москва)
- **IP**: 109.73.206.169
- **Стек**: nginx → gunicorn → Flask
- **БД**: SQLite (devices.db)

## Деплой

На сервере:
```bash
cd /opt/phonedeck
git pull
cd frontend && npm ci && CI=false npm run build && cd ..
cp -r frontend/build ./build
sudo systemctl restart phonedeck
```

## Библиотеки Arduino

Установка: Arduino IDE → Sketch → Include Library → Add .ZIP Library

| Библиотека | Версия | Назначение |
|------------|--------|------------|
| ArduinoJson | 7.0.4 | Формирование JSON для POST |
| TimeLib | master | Преобразование Unix времени |
| iarduino_I2C_4LED | 1.0.2 | Управление I2C дисплеями |
| iarduino_RTC | 2.0.0 | Работа с часами DS3231 |

## Настройка ESP8266

В файле `arduino/NodeMCU_updated/NodeMCU_updated.ino` указать WiFi:
```cpp
#define WIFI_SSID "название_сети"
#define WIFI_PASSWORD "пароль"
```

Плата в Arduino IDE: **NodeMCU 1.0 (ESP-12E Module)**
