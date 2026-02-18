from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.queue_manager import QueueManager

queue_manager = QueueManager()

@Client.on_message(filters.command("queue") & filters.group)
async def queue_command(client: Client, message: Message):
    """/queue komutu - Mevcut kuyruğu göster"""
    chat_id = message.chat.id
    
    queue = queue_manager.get_queue(chat_id)
    
    if not queue:
        await message.reply_text(
            "📦 **Kuyruk boş!**\n\n"
            "🎵 Müzik eklemek için `/play <şarkı adı>` komutunu kullanın."
        )
        return
    
    # Kuyruk listesini hazırla
    text = "📋 **Müzik Kuyruğu:**\n\n"
    
    for i, song in enumerate(queue, 1):
        if i == 1:
            text += f"▶️ **Şimdi çalınıyor:**\n"
        else:
            text += f"\n**{i}.** "
        
        text += f"🎵 {song['title']}\n"
        text += f"⏱ {song['duration']}\n"
        text += f"👤 {song['requested_by']}\n"
    
    text += f"\n📄 **Toplam:** {len(queue)} şarkı"
    
    await message.reply_text(text)

queue_command = Client.on_message(filters.command("queue") & filters.group)(queue_command)
