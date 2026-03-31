from aiogram.fsm.state import State, StatesGroup

class GptStates(StatesGroup):
    chatting = State()

class TalkStates(StatesGroup):
    choosing_person = State()
    chatting = State()