
from aiogram import Bot,Dispatcher,F
from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from config import *

PLANS={
' پلن 1 ماهه 10 گیگ':'120000',
'پلن 1 ماهه گیگ 20 گیگ ':'220000',
'پلن 1 ماهه گیگ 30 گیگ ':'330000',
'پلن 1 ماهه گیگ 40 گیگ ':'440000',
'پلن 1 ماهه گیگ 50 گیگ ':'550000',
'پلن 1 ماهه گیگ 100 گیگ ':'800000'
}

class Order(StatesGroup):
    plan=State()
    username=State()
    receipt=State()

bot=Bot(BOT_TOKEN)
dp=Dispatcher(storage=MemoryStorage())

kb=ReplyKeyboardMarkup(keyboard=[
[KeyboardButton(text='🛒 خرید سرویس')],
[KeyboardButton(text='🆘 پشتیبانی')]],resize_keyboard=True)

@dp.message(CommandStart())
async def start(m:Message):
    await m.answer('خوش آمدید',reply_markup=kb)

@dp.message(F.text=='🆘 پشتیبانی')
async def support(m:Message):
    await m.answer(SUPPORT)

@dp.message(F.text=='🛒 خرید سرویس')
async def buy(m:Message,state:FSMContext):
    await state.set_state(Order.plan)
    await m.answer("\n".join([f"{k} - {v}" for k,v in PLANS.items()]))

@dp.message(Order.plan)
async def plan(m:Message,state:FSMContext):
    await state.update_data(plan=m.text)
    await state.set_state(Order.username)
    await m.answer('نام کاربری را ارسال کنید')

@dp.message(Order.username)
async def usern(m:Message,state:FSMContext):
    data=await state.get_data()
    await state.update_data(username=m.text)
    await state.set_state(Order.receipt)
    await m.answer(
    f'کارت: {CARD_NUMBER}\nصاحب کارت: {CARD_OWNER}\nرسید را ارسال کنید')

@dp.message(Order.receipt,F.photo)
async def receipt(m:Message,state:FSMContext):
    data=await state.get_data()
    await bot.send_photo(ADMIN_ID,m.photo[-1].file_id,
    caption=f"سفارش جدید\n{data}")
    await m.answer('رسید ثبت شد')
    await state.clear()

if __name__=='__main__':
    dp.run_polling(bot)
