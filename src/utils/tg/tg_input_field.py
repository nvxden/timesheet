import random

from typing import Callable, Optional, List

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.entities.message_maker.accessory import send_message
from src.utils.tg.tg_state import TgState
from src.utils.tg.value_validators import Validator, ValidatorObject


class InputFieldButton:
  def __init__(self, title: str, data):
    self.title = title
    self.data = data
    self.qb = str(random.random())


class TgInputField(TgState):
  def __init__(
    self,
    tg: TeleBot,
    chat,
    greeting: str,
    validator: Validator,
    on_field_entered: Callable,
    terminate_message: str = None,
    buttons: List[List[InputFieldButton]] = None,
  ):
    self.tg = tg
    self.chat = chat
    self.validator = validator
    self.onFieldEntered = on_field_entered
    self.terminateMessage = terminate_message
    self.buttons = buttons
    super().__init__(lambda: send_message(tg=self.tg,
                                          chat_id=self.chat,
                                          text=greeting,
                                          reply_markup=self._makeMarkup(),
                                          emoji='edit'))

  # OVERRIDE METHODS
  def _onTerminate(self):
    if self.terminateMessage is not None:
      send_message(tg=self.tg,
                   chat_id=self.chat,
                   text=self.terminateMessage,
                   emoji='warning')
      
  def _handleMessage(self, m: Message):
    answer = self.validator.validate(ValidatorObject(message=m))
    if not answer.success:
      send_message(tg=self.tg,
                   chat_id=self.chat,
                   text=answer.error,
                   emoji=answer.emoji)
    else:
      self.onFieldEntered(answer.data)
    return True

  def _handleCallbackQuery(self, q: CallbackQuery):
    for row in self.buttons:
      for button in row:
        if q.data == button.qb:
          self.tg.answer_callback_query(callback_query_id=q.id,
                                        text=f'?????????????? {button.title}')
          self.onFieldEntered(button.data)
          return True
    return False


  # SERVICE METHODS
  def _makeMarkup(self) -> Optional[InlineKeyboardMarkup]:
    if self.buttons is None:
      return None
    markup = InlineKeyboardMarkup()
    for row in self.buttons:
      markup.add(*[InlineKeyboardButton(text=b.title, callback_data=b.qb)
                   for b in row],
                 row_width=len(row))
    return markup

  def _handleMessageBefore(self, m: Message) -> bool:
    pass
