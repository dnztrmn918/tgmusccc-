from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.youtube import search_youtube, download_audio
from bot.utils.queue_manager import QueueManager
import asyncio

# Queue manager (her grup için ayrı kuyruk)
queue_manager = QueueManager()

async def play_command(client: Client, message: Message):
    """/play komutu - Müzik çal"""
    
    # Şarkı adını al
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **Kullanım:** `/play <şarkı adı>`\n"
            "🔍 **Örnek:** `/play Tarkan Şımarık`"
        )
        return
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    
    # Arama mesajı
    status = await message.reply_text(f"🔍 **Aranıyor:** `{query}`")
    
    try:
        # YouTube'da ara
        result = await search_youtube(query)
        
        if not result:
            await status.edit_text("❌ **Sonuç bulunamadı!** Lütfen başka bir şarkı deneyin.")
            return
        
        # İndirme başlat
        await status.edit_text(
            f"🎵 **Bulunan:** {result['title']}\n"
            f"⏱ **Süre:** {result['duration']}\n"
            f"📥 **İndiriliyor...**"
        )
        
        # Ses dosyasını indir
        file_path = await download_audio(result['video_id'])
        
        if not file_path:
            await status.edit_text("❌ **İndirme hatası!** Lütfen tekrar deneyin.")
            return
        
        # Kuyruğa ekle
        queue_manager.add_to_queue(chat_id, {
            'title': result['title'],
            'duration': result['duration'],
            'file_path': file_path,
            'requested_by': message.from_user.mention
        })
        
        # Kuyruktaki pozisyonu göster
        position = queue_manager.get_queue_position(chat_id, file_path)
        
        if position == 0:
            await status.edit_text(
                f"▶️ **Şimdi çalınıyor:**\n"
                f"🎵 {result['title']}\n"
                f"⏱ {result['duration']}\n"
                f"👤 {message.from_user.mention}"
            )
            # TODO: Burada gerçek çalma işlemi yapılacak (py-tgcalls ile)
        else:
            await status.edit_text(
                f"✅ **Kuyruğa eklendi!**\n"
                f"🎵 {result['title']}\n"
                f"⏱ {result['duration']}\n"
                f"📋 Sıra: #{position + 1}\n"
                f"👤 {message.from_user.mention}"
            )
    
    except Exception as e:
        await status.edit_text(f"❌ **Hata:** `{str(e)}`")
