from pyrogram import Client
from pyrogram.types import Message

async def cookie_command(client: Client, message: Message):
    """/cookie komutu - Cookie hakkında bilgi"""
    
    await message.reply_text(
        "🍪 **YouTube Cookie Hakkında**\n\n"
        "Bazı YouTube videoları (yaş kısıtlamalı, bölgesel vb.) "
        "indirmek için cookie gerektirir.\n\n"
        "**Cookie Nasıl Alınır:**\n\n"
        "**PC/Laptop:**\n"
        "1. Chrome/Firefox'a 'Get cookies.txt LOCALLY' eklentisini yükleyin\n"
        "2. YouTube'a giriş yapın\n"
        "3. Eklenti ile cookies.txt dosyasını indirin\n"
        "4. Dosyayı bot dizinine koyun\n\n"
        "**iPhone/iPad:**\n"
        "1. Safari'de YouTube'a giriş yapın\n"
        "2. Mac varsa: Safari Web Inspector ile alınabilir\n"
        "3. Alternatif: Bir arkadaşınızdan cookie alabilirsiniz\n\n"
        "**Android:**\n"
        "1. Kiwi Browser yükleyin\n"
        "2. 'Get cookies.txt LOCALLY' eklentisini yükleyin\n"
        "3. YouTube'a giriş yapıp cookie alın\n\n"
        "⚠️ **Önemli:** Cookie dosyasını `cookies.txt` olarak "
        "bot'un ana dizinine yerleştirin."
    )
