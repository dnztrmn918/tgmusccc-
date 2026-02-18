from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

async def start_command(client: Client, message: Message):
    """/start komutu - Hoş geldin mesajı"""
    
    buttons = []
    
    if Config.SUPPORT_GROUP:
        buttons.append(InlineKeyboardButton("👥 Destek Grubu", url=Config.SUPPORT_GROUP))
    if Config.SUPPORT_CHANNEL:
        buttons.append(InlineKeyboardButton("📢 Kanal", url=Config.SUPPORT_CHANNEL))
    
    keyboard = InlineKeyboardMarkup([buttons]) if buttons else None
    
    await message.reply_text(
        f"🎵 **Müzik Botu'na Hoş Geldiniz!**\n\n"
        f"YouTube'dan müzik arayıp grup sesli sohbetlerinde çalabilirsiniz.\n\n"
        f"**🎯 Komutlar:**\n"
        f"`/play <şarkı adı>` - Müzik ara ve çal\n"
        f"`/pause` - Müziği duraklat\n"
        f"`/resume` - Müziğe devam et\n"
        f"`/skip` - Şarkıyı atla\n"
        f"`/stop` - Müziği durdur\n"
        f"`/queue` - Kuyruğu gör\n"
        f"`/cookie` - Cookie bilgisi\n\n"
        f"**💡 Kullanım:**\n"
        f"1. Botu grubunuza ekleyin\n"
        f"2. Bota yönetici yetkisi verin\n"
        f"3. `/play şarkı adı` yazın\n\n"
        f"✨ İyi dinlemeler!",
        reply_markup=keyboard
    )
