import  logging
from telegram import ReplyKeyboardRemove, Update, CallbackQuery
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from dataclasses import dataclass

from telegram_client.app.backend import BaseBackend
import telegram_client.app.keyboards as kb
from telegram_client.constants.texts import texts
from telegram_client.app.utils import name_to_reg

class Client:

    @dataclass()
    class States:
        MAIN_MENU: int
        QUERY_INPUT: int
        PROCEED_QUERY_INPUT: int
        EMOTION: int
        BODY: int
        REPLACEMENT: int

    def __init__(self, 
                 backend: BaseBackend,
                 token: str,
        ) -> None:
        self.backend = backend
        self.application = Application.builder().token(token).build()
        self.states = self.get_states()

    def get_states(self):
        states = self.States(*range(6))
        return states

    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        text = texts['start_text']

        markup = kb.get_start_keyboard()

        await update.message.reply_text(
            text,
            reply_markup=markup
        )

        return self.states.MAIN_MENU

    async def ask_query_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        text = texts['input_query']

        await update.message.reply_text(
                text,
                reply_markup=ReplyKeyboardRemove(),
        )

        return self.states.QUERY_INPUT

    async def proceed_query_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        input_text = update.message.text

        response = self.backend.call(input_text)
        markup = kb.get_start_keyboard()

        await update.message.reply_text(
                response,
                reply_markup=markup,
        )

        return self.states.MAIN_MENU

    async def done(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return ConversationHandler.END

    def build_conversation_handler(self) -> ConversationHandler:
        conv_handler = ConversationHandler(
            allow_reentry=True,
            entry_points=[
                    CommandHandler("start", self.main_menu),
            ],
            states={
                self.states.MAIN_MENU: [
                    MessageHandler(filters.Regex(name_to_reg(texts['run_query_button'])), self.ask_query_input),
                    MessageHandler(filters.TEXT, self.main_menu)
                ],
                self.states.QUERY_INPUT: [
                    MessageHandler(filters.TEXT, self.proceed_query_input)
                ]
            },
            fallbacks=[MessageHandler(filters.Regex("^Done$"), self.done)],
        )

        return conv_handler

    def build_application(self):
        conv_handler = self.build_conversation_handler()
        self.application.add_handler(conv_handler)
        self.application.run_polling(drop_pending_updates=True)

