import os
from PIL import Image
from pyrogram import Client,filters 
from pyrogram.types import (InlineKeyboardButton,  InlineKeyboardMarkup)

from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

TOKEN = os.environ.get("TOKEN", "")

API_ID = int(os.environ.get("API_ID", 12345))

API_HASH = os.environ.get("API_HASH", "")
app = Client(
        "pdf",
        bot_token=TOKEN,api_hash=API_HASH,
            api_id=API_ID
    )


LIST = {}

@app.on_message(filters.command(['start']))
async def start(client, message):
 await message.reply_text(text =f"""مرحبا 😇 {message.from_user.first_name } بك في بوت pdf
أنا بوت أقوم بتحويل الصورة الى pdf
وايظا اقوم بضغط ملف pdf اذا كان حجمة كبير 
فقط ارسلي pdf
                    """,reply_to_message_id = message.message_id ,  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("دعم 💊" ,url="https://t.me/ooonn2") ],
                 [InlineKeyboardButton("قناة البوت 🔊", url="https://t.me/enghussainh") ]       ]        ) )




@app.on_message(filters.private & filters.photo)
async def pdf(client,message):
 
 if not isinstance(LIST.get(message.from_user.id), list):
   LIST[message.from_user.id] = []

  
 
 file_id = str(message.photo.file_id)
 ms = await message.reply_text("تحويل الى pdf📙......")
 file = await client.download_media(file_id)
 
 image = Image.open(file)
 img = image.convert('RGB')
 LIST[message.from_user.id].append(img)
 await ms.edit(f"{len(LIST[message.from_user.id])} اذا تريد بعد أرسل صور للبوت 🖼\n\n **إذا  كملت إضغط  هذا أمر  👉 /convert** ")
 

@app.on_message(filters.command(['convert']))
async def done(client,message):
 images = LIST.get(message.from_user.id)

 if isinstance(images, list):
  del LIST[message.from_user.id]
 if not images:
  await message.reply_text( "!!لا يوجد  صورة")
  return

 path = f"{message.from_user.id}" + ".pdf"
 images[0].save(path, save_all = True, append_images = images[1:])
 
 await client.send_document(message.from_user.id, open(path, "rb"), caption = "هذا ملف جاهز 😇")
 os.remove(path)
 
 
 
 
app.run()
