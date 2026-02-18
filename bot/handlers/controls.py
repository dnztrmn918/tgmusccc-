from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from bot.utils.queue_manager import queue_manager
from bot.core.call import call_manager
import os
from config import Config

async def pause_command(client: Client, message: Message):
    """/pause komutu - Müziği duraklat"""
    try:
        await client.get_chat(message.chat.id)
    except (PeerIdInvalid, ChannelInvalid, ValueError, KeyError):
        pass
    
    chat_id = message.chat.id
    
    if not call_manager.is_playing(chat_id):
        await message.reply_text("❌ **Şu anda çalan müzik yok!**")
        return
    
    success = await call_manager.pause(chat_id)
    
    if success:
        await message.reply_text("⏸ **Müzik duraklatıldı.**\n\nDevam etmek için: /resume")
    else:
        await message.reply_text("❌ **Duraklatma hatası!**")

async def resume_command(client: Client, message: Message):
    """/resume komutu - Müziğe devam et"""
    chat_id = message.chat.id
    
    if not call_manager.is_paused(chat_id):
        await message.reply_text("❌ **Duraklatılmış müzik yok!**")
        return
    
    success = await call_manager.resume(chat_id)
    
    if success:
        await message.reply_text("▶️ **Müzik devam ediyor.**")
    else:
        await message.reply_text("❌ **Devam ettirme hatası!**")

async def stop_command(client: Client, message: Message):
    """/stop komutu - Müziği durdur ve sesli sohbetten ayrıl"""
    chat_id = message.chat.id
    
    # Kuyruğu temizle
    queue = queue_manager.get_queue(chat_id)
    queue_manager.clear_queue(chat_id)
    
    # İndirilen dosyaları temizle
    for song in queue:
        try:
            if os.path.exists(song['file_path']):
                os.remove(song['file_path'])
        except:
            pass
    
    # Sesli sohbetten ayrıl
    await call_manager.stop(chat_id)
    
    await message.reply_text(
        "⏹ **Müzik durduruldu.**\n"
        "👋 Sesli sohbetten ayrıldım.\n"
        "🗑 Kuyruk temizlendi."
    )

async def skip_command(client: Client, message: Message):
    """/skip komutu - Şarkıyı atla"""
    chat_id = message.chat.id
    
    current = queue_manager.get_current_song(chat_id)
    if not current:
        await message.reply_text("❌ **Şu anda çalan müzik yok!**")
        return
    
    # Mevcut dosyayı sil
    try:
        if os.path.exists(current['file_path']):
            os.remove(current['file_path'])
    except:
        pass
    
    # Sonraki şarkıya geç
    next_song = queue_manager.skip_song(chat_id)
    
    if next_song:
        success = await call_manager.play(chat_id, next_song['file_path'])
        if success:
            await message.reply_text(
                f"⏭ **Atlandı!**\n\n"
                f"▶️ **Şimdi çalınıyor:**\n"
                f"🎵 {next_song['title']}\n"
                f"⏱ {next_song['duration']}"
            )
        else:
            await message.reply_text("❌ **Sonraki şarkı çalınamadı!**")
    else:
        await call_manager.stop(chat_id)
        await message.reply_text(
            "⏭ **Atlandı!**\n\n"
            "📋 Kuyrukta başka şarkı yok.\n"
            "👋 Sesli sohbetten ayrıldım."
        )
