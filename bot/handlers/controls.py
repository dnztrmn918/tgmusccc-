from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.queue_manager import QueueManager

queue_manager = QueueManager()

@Client.on_message(filters.command("pause") & filters.group)
async def pause_command(client: Client, message: Message):
    """/pause komutu - Müziği duraklat"""
    chat_id = message.chat.id
    
    # TODO: py-tgcalls ile duraklat
    await message.reply_text("⏸ **Müzik duraklatildı.**")

@Client.on_message(filters.command("resume") & filters.group)
async def resume_command(client: Client, message: Message):
    """/resume komutu - Müziğe devam et"""
    chat_id = message.chat.id
    
    # TODO: py-tgcalls ile devam et
    await message.reply_text("▶️ **Müzik devam ediyor.**")

@Client.on_message(filters.command("stop") & filters.group)
async def stop_command(client: Client, message: Message):
    """/stop komutu - Müziği durdur ve sesli sohbetten ayrıl"""
    chat_id = message.chat.id
    
    # Kuyruğu temizle
    queue_manager.clear_queue(chat_id)
    
    # TODO: py-tgcalls ile durdur ve ayrıl
    await message.reply_text(
        "⏹ **Müzik durduruldu.**\n"
        "👋 Sesli sohbetten ayrıldım.\n"
        "🗑 Kuyruk temizlendi."
    )

pause_command = Client.on_message(filters.command("pause") & filters.group)(pause_command)
resume_command = Client.on_message(filters.command("resume") & filters.group)(resume_command)
stop_command = Client.on_message(filters.command("stop") & filters.group)(stop_command)
