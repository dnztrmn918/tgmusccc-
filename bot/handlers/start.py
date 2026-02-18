from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """/start komutu - Özel mesajlarda hoş geldin mesajı"""
    
    user = message.from_user
    
    # Hoş geldin mesajı
    text = f"""
🎵 **Merhaba {user.mention}!**

Ben bir Telegram Müzik Botu. YouTube ve SoundCloud'dan müzik çalabilirim.

**🎶 Kullanılabilir Komutlar:**

▫️ `/play <şarkı adı>` - Müzik oynat
▫️ `/pause` - Müziği duraklat
▫️ `/resume` - Müziğe devam et
▫️ `/stop` - Müziği durdur ve sesli sohbetten ayrıl
▫️ `/queue` - Şu anki müzik kuyruğunu gör

**💡 Nasıl Kullanılır?**
1. Beni grubunuza ekleyin
2. Beni yönetici yapın
3. Sesli sohbete katılın
4. `/play <şarkı adı>` komutunu kullanın

✨ İyi eğlenceler!
    """.strip()
    
    # Butonlar
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 Komutlar", callback_data="help"),
                InlineKeyboardButton("ℹ️ Hakkında", callback_data="about")
            ]
        ]
    )
    
    # Destek linkleri varsa ekle
    if Config.SUPPORT_GROUP or Config.SUPPORT_CHANNEL:
        support_buttons = []
        if Config.SUPPORT_GROUP:
            support_buttons.append(InlineKeyboardButton("👥 Destek Grubu", url=Config.SUPPORT_GROUP))
        if Config.SUPPORT_CHANNEL:
            support_buttons.append(InlineKeyboardButton("📢 Kanal", url=Config.SUPPORT_CHANNEL))
        buttons.inline_keyboard.append(support_buttons)
    
    await message.reply_text(text, reply_markup=buttons)

start_command = filters.create(lambda _, __, m: m.text and m.text.startswith("/start"))
start_command = Client.on_message(filters.command("start") & filters.private)(start_command)
