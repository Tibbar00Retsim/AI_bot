from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import text
import g4f
import g4f.image as g4f_image
import logging

# Настройка журналирования
logging.basicConfig(level=logging.INFO)

class MyBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dp = Dispatcher(bot=self.bot)
        self.provider = g4f.Provider.Bing
        self.setup_handlers()

    async def send_response(self, message: types.Message, user_message: str):
        logging.info(f"Received message: {user_message}")
        await message.answer_chat_action(types.ChatActions.TYPING)
        response = await g4f.ChatCompletion.create_async(model="gpt-4", messages=[{"role": "user", "content": user_message}], provider=self.provider)
        logging.info(f"Sending response: {response}")
        await message.answer(response)

    def setup_handlers(self):
        @self.dp.message_handler(content_types=types.ContentType.TEXT)
        async def handle_message(message: types.Message):
            await self.send_response(message, message.text)

        @self.dp.message_handler(commands=["start"])
        async def start(message: types.Message):
            logging.info("Received start command")
            await message.answer(text("Привет! Я ваш бот Bing."))

        @self.dp.message_handler(commands=["image"])
        async def image(message: types.Message):
            query = message.get_args()
            logging.info(f"Received image command with query: {query}")
            if query:
                result = await g4f_image.ImageCompletion.create_async(model="dalle-3", query=query, provider=self.provider)
                await message.answer_photo(result)
            else:
                await message.answer(text("Пожалуйста, укажите текстовый запрос для изображения после команды /image"))

    def main(self):
        self.dp.start_polling()
        logging.info("Бот запущен и работает...")

if __name__ == '__main__':
    bot = MyBot('token')
    bot.main()
