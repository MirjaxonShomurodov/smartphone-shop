from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CallbackContext
import keyboards
from db import get_phone_by_id,get_items,clear_items,add_item

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        text=f'Hello welcome to our channel 👨🏻‍💻 {user.first_name}.',
        reply_markup=keyboards.home_keyboard()
    )
def shop(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Hello, choose which campaign you need.',
        reply_markup=keyboards.brends_keyboard(),
    )
def cart(update:Update,context:CallbackContext):
    user = update.effective_user
    
    items = get_items(user_id=user.id)
    text = "Your basket\n\n"
    total = 0

    for item in items:
        phone = get_phone_by_id(item['brend'],item['phone_id'])
        total += phone['price']

        text += f"-> {phone.doc_id} {phone['name']} - {phone['price']}\n"

    text += f"\ntotal: {total}"


    update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('buy',callback_data='buy'),
                    InlineKeyboardButton('clear',callback_data='clear-basket')
                ],
                [
                    InlineKeyboardButton('close',callback_data='close-basket')
                ]
            ]
        )
    )

    
def phones(update:Update,context:CallbackContext):
    brend = update.callback_query.data.split(':')[1]
    update.callback_query.message.reply_text(
         text = 'Hello, choose what phone you need.',
        reply_markup=keyboards.phones_keyboard(brend)
    )

def send_phone(update:Update,context:CallbackContext):
    brend,doc_id = update.callback_query.data.split(':')[1:]
    
    phone = get_phone_by_id(brend, doc_id)
    
    update.callback_query.message.reply_photo(
        photo=phone['img_url'],
        caption=f'📲 Phone: {phone["name"]}\n🌈 Rangi: {phone["color"]}\ncompany: {phone["company"]}\nRAM: {phone["RAM"]}\n💾 Xotirasi: {phone["memory"]}\n💰 Narxi:{phone["price"]}',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('add cart',callback_data=f'add:{brend}:{doc_id}'),
                    InlineKeyboardButton('close',callback_data=f'close')
                ]
            ]
        )
    )    

def close_phone(update: Update, context: CallbackContext):
    update.callback_query.message.delete()

def add_cart(update: Update, context: CallbackContext):
    user = update.effective_user
    brend, doc_id = update.callback_query.data.split(':')[1:]

    add_item(user.id, brend, doc_id)

    update.callback_query.answer(text='added item.', show_alert=True)

def clear_basket(update: Update, context: CallbackContext):
    user = update.effective_user

    clear_items(user.id)

    update.callback_query.answer(text='removed items.', show_alert=True)
    
    close_phone(update, context)



def contact(update:Update,context:CallbackContext):
    user = update.message.from_user
    update.message.reply_contact(
        
        phone_number="998888980242",
        first_name="Codeakademya",
    )

def about(update:Update,context:CallbackContext):
    user = update.message.from_user
    update.message.reply_html(
        text=f"Hello, sorry, we cannot provide information about ourselves🤫.{user.first_name}",
        reply_markup=keyboards.home_keyboard()
    )
def send_buy(update:Update,context:CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        text=f"{user.first_name} raxmat bizning Smartpgone_shop botimizga yana tashrif buyiring. https://t.me/Mirjaxon2003 shu kassa orqali buyurtma qilganlganlarizni tulaysiz... ",
        reply_markup=keyboards.home_keyboard()
    )
