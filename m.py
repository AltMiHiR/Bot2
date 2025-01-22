import pytz
import logging
import asyncio
import threading

from pyrogram import Client, filters, idle
from pyrogram.types import Message

from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient



IST = pytz.timezone('Asia/Kolkata')

_mongo_async_ = AsyncIOMotorClient("mongodb+srv://MIHIRxKHUSHI:print('MIKU1311')@thealtron.rwuawpe.mongodb.net/?retryWrites=true&w=majority")
TrackDataCol = _mongo_async_["MFBot"]['TrackData']

ACCOUNT = {
    "session": "BQGMcpgAfVL4GMkEgTuTz82qRt6NkOTDJf19TAJ7X-TpIFCYed8qXib4QNKL_W9WEsk3LQAzIp6DCJXN5sC53dbkahzkHN0Ltxp4NCDcEo83fis4EA2s9i0AMsXa8UqChomqrfIIPzOWHqqs9o9laSGtl3apQAMnunQWAr9iE5Ikh6t7wdtGAirsWa8bkE_5atsIRMzvkIVzDU__Yn5kq9L6lPkAQxiEFtQ92H3tSHr8f6Xmpc2YRku8TjipXWxVF7xYzLkEPXRSY78b3TjolRB6KQME6Tks5aX0EsKRgPp51dT7Lu7KpRKrJl_yykEPYhz7YHlk_obuDLxjOiw7SWDMbVzN3gAAAAHU-8UVAA",
    "phone_number": "+919756740328"
}

CHATS = {
    -1001293195336: "@MADEITOUTTHASTONE",
    -1001232993323: "@kofecktkassin",
    -1001147510917: "https://t.me/joinchat/McFg_URloIV0FesEJDfAAw",
    -1001713249177: "https://t.me/joinchat/LxwyGSxGIrIzOGE1",
    -1002148525952: "https://t.me/joinchat/Jzyphd-fWPwwZWNl"
}

class ThreadSafeList(list):
    def __init__(self, *args):
        super().__init__(*args)
        self._lock = threading.Lock()

    def append(self, item):
        with self._lock:
            super().append(item)

    def extend(self, iterable):
        with self._lock:
            super().extend(iterable)

    def copy_with_clear(self):
        with self._lock:
            data = super().copy()
            super().clear()
            return data

    def copy(self):
        with self._lock:
            return super().copy()

    def remove(self, item):
        with self._lock:
            super().remove(item)

    def pop(self, index=-1):
        with self._lock:
            return super().pop(index)

    def clear(self):
        with self._lock:
            super().clear()

    def __contains__(self, item):
        with self._lock:
            return super().__contains__(item)

    def __iter__(self):
        with self._lock:
            return iter(super().copy())

    def __len__(self):
        with self._lock:
            return super().__len__()

    def __getitem__(self, index):
        with self._lock:
            return super().__getitem__(index)

    def __setitem__(self, index, value):
        with self._lock:
            super().__setitem__(index, value)

    def __delitem__(self, index):
        with self._lock:
            super().__delitem__(index)


DATA = ThreadSafeList()

app = Client(ACCOUNT["phone_number"], session_string=ACCOUNT["session"], max_message_cache_size=0)

@app.on_message(filters.group & filters.user([5961091462, 277756078, 756558173, 126203394, 108918720]))
async def _tracker(client: Client, message: Message):
    data = {
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "message_id": message.id,
        "timestamp": int(message.date.timestamp())
    }
    DATA.append(data)


async def main():
    await app.start()
    print("USERBOT STARTED!\n")

    while True:
        await asyncio.sleep(1800)

        if len(DATA) > 0:
            data = DATA.copy_with_clear()
            await TrackDataCol.insert_many(data)
            day = datetime.now(IST)
            print(f"ADDED_{len(data)}_DOCS - {day.strftime('%d-%m-%Y %H:%M:%S')}")
        else:
            day = datetime.now(IST)
            print(f"ADDED_0_DOCS - {day.strftime('%d-%m-%Y %H:%M:%S')}")

    await app.stop()
    print("USERBOT STOPPED!")


logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
