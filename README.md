<p align="center">

 <img src="https://i.imgur.com/rSyq3MW.png" alt="The Documentation Compendium"></a>
</p>

<h3 align="center">screen-ocr</h3>
<p align = "center">Tool for ...</p>

 <img src="http://recordit.co/WPvGYmyWrY" alt="The Documentation Compendium"></a>
<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/badge/license-CC0-blue.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

</div>

---

<p align = "center">Tool for ...</p>


## Приступим к работе

- [Авторизация бота и запуск](#bot_init)

- [Связываем события с функциями](#bind)
  - [Связываем команды - bind_command()](#bind_command)
  - [Связываем callback кнопки - bind_callback()](#bind_callback)
  - [Связываем события целиком - bind_event()](#bind_event)
- [Обработка событий](#events)
  - [Обработка текста и команд](#text_handler)
  - [Обработка фотографий](#photo_handler)
  - [Обработка документов](#document_handler)
  - [Обработка голосовых сообщений](#voice_handler)
  - [Обработка незарегистрированных команд](#unregistred_commands)
  - [Обработка незарегистрированных событий](#unregistred_events)
- [Отправка сообщений - send_message() ](#send_message)
- [Отправка фотографий - send_photo() ](#send_photo)
- [Отправка документов - send_document() ](#send_document)
- [Работа с клавиатурами](#keyboards)
  - [Inline клавиатуры](#inline_keyboards)
  - [Reply клавиатуры](#reply_keyboards)
- [Ожидание события от пользователя - bind_input()](#input)
- [Скачивание файлов - download_file()](#download_files)
- [Обратная связь](#feedback)
- [Acknowledgements](#acknowledgements)


## Авторизация бота и запуск <a name = "bot_init"></a>

Чтобы авторизировать бота, достаточно передать его токен при запуске бота 
```python
from lightbot import bot
bot.run(token='55950...YoxWc')
```
Запуск:
```python
def run(show_event=False)
``` 
Метод запускает бота, он должен вызыватся самым последним.
Принимает параметр show_event и token. Когда show_event=True, печатает в консоль ответ от телеграма.
