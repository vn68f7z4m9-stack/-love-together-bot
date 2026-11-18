
import os
import json
import time
import urllib.request
import urllib.parse

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN")

API = f"https://api.telegram.org/bot{TOKEN}/"

def telegram(method, data=None):
    body = urllib.parse.urlencode(data or {}).encode()
    req = urllib.request.Request(API + method, data=body)
    with urllib.request.urlopen(req, timeout=40) as response:
        return json.loads(response.read())

def send(chat_id, text, keyboard=None):
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    telegram("sendMessage", data)

def main():
    offset = 0
    print("Love Together запущен!")

    while True:
        try:
            updates = telegram("getUpdates", {
                "offset": offset,
                "timeout": 30
            })

            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                text = message.get("text", "")

                if not chat_id:
                    continue

                if text.startswith("/start"):
                    send(
                        chat_id,
                        "❤️ Добро пожаловать в Love Together!\n\n"
                        "Ваше маленькое пространство для двоих.",
                        {
                            "keyboard": [
                                [{"text": "💑 Создать пару"}],
                                [{"text": "💌 Пригласить половинку"}],
                                [{"text": "📅 Дата отношений"}],
                                [{"text": "💗 Послание дня"}]
                            ],
                            "resize_keyboard": True
                        }
                    )

                elif text == "💑 Создать пару":
                    send(chat_id, "💑 Скоро здесь можно будет создать вашу пару!")

                elif text == "💌 Пригласить половинку":
                    send(chat_id, "💌 Скоро здесь появится приглашение для любимого человека!")

                elif text == "📅 Дата отношений":
                    send(chat_id, "📅 Скоро здесь появится ваш счётчик отношений!")

                elif text == "💗 Послание дня":
                    send(chat_id, "💗 Ты — самое прекрасное, что случилось в моей жизни!")

                else:
                    send(chat_id, "Нажми /start, чтобы открыть меню ❤️")

        except Exception as error:
            print("Ошибка:", error)
            time.sleep(5)

if __name__ == "__main__":
    main()
