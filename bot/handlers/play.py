from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from bot.utils.youtube import search_youtube, download_audio, is_youtube_cookie_error
from bot.utils.soundcloud import search_soundcloud, download_soundcloud_audio
from bot.utils.queue_manager import queue_manager
from bot.core.call import call_manager
import os

async def play_command(client: Client, message: Message):
    # Peer ID hatasını önlemek için chat'i çözümle
    try:
        await client.get_chat(message.chat.id)
    except (PeerIdInvalid, ChannelInvalid, ValueError, KeyError):
        pass  # Hata olsa bile devam et
    """/play komutu - Müzik çal (YouTube + SoundCloud fallback)"""
    
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
        result = None
        file_path = None
        used_soundcloud = False
        
        # 1. Önce YouTube'da ara
        await status.edit_text(f"🔍 **YouTube'da aranıyor:** `{query}`")
        result = await search_youtube(query)
        
        if result:
            # YouTube'dan indirmeyi dene
            await status.edit_text(
                f"🎵 **Bulunan:** {result['title']}\n"
                f"⏱ **Süre:** {result['duration']}\n"
                f"📥 **YouTube'dan indiriliyor...**"
            )
            file_path = await download_audio(result['video_id'])
        
        # 2. YouTube başarısız olduysa SoundCloud'a geç
        if not file_path:
            youtube_error = is_youtube_cookie_error()
            
            if youtube_error:
                await status.edit_text(
                    f"⚠️ **YouTube cookie hatası!**\n"
                    f"🔄 **SoundCloud'da aranıyor:** `{query}`"
                )
            else:
                await status.edit_text(
                    f"⚠️ **YouTube'dan indirilemedi**\n"
                    f"🔄 **SoundCloud'da aranıyor:** `{query}`"
                )
            
            # SoundCloud'da ara
            result = await search_soundcloud(query)
            
            if result:
                used_soundcloud = True
                await status.edit_text(
                    f"🎵 **SoundCloud'da bulundu:** {result['title']}\n"
                    f"⏱ **Süre:** {result['duration']}\n"
                    f"📥 **İndiriliyor...**"
                )
                file_path = await download_soundcloud_audio(result['url'], result['track_id'])
        
        # 3. Her iki platform da başarısız olduysa
        if not result or not file_path:
            await status.edit_text(
                "❌ **Şarkı bulunamadı veya indirilemedi!**\n\n"
                "💡 **Öneriler:**\n"
                "- Farklı bir şarkı adı deneyin\n"
                "- Şarkıyı İngilizce aramayı deneyin\n"
                "- Cookie ekleyerek YouTube erişimini artırın (`/cookie`)"
            )
            return
        
        # Kuyruğa ekle
        song_data = {
            'title': result['title'],
            'duration': result['duration'],
            'file_path': file_path,
            'requested_by': message.from_user.mention,
            'source': 'SoundCloud' if used_soundcloud else 'YouTube'
        }
        queue_manager.add_to_queue(chat_id, song_data)
        
        # Kuyruktaki pozisyonu göster
        position = queue_manager.get_queue_position(chat_id, file_path)
        source_emoji = "☁️" if used_soundcloud else "▶️"
        source_name = "SoundCloud" if used_soundcloud else "YouTube"
        
        if position == 0:
            # Sesli sohbette çal
            await status.edit_text(
                f"🔊 **Sesli sohbete bağlanılıyor...**\n"
                f"🎵 {result['title']}"
            )
            
            success = await call_manager.play(chat_id, file_path)
            
            if success:
                await status.edit_text(
                    f"{source_emoji} **Şimdi çalınıyor ({source_name}):**\n"
                    f"🎵 {result['title']}\n"
                    f"⏱ {result['duration']}\n"
                    f"👤 {message.from_user.mention}"
                )
            else:
                await status.edit_text(
                    f"❌ **Sesli sohbete bağlanılamadı!**\n\n"
                    f"💡 **Kontrol edin:**\n"
                    f"- Botun yönetici olduğundan emin olun\n"
                    f"- Sesli sohbet izinlerini kontrol edin\n"
                    f"- Grupda sesli sohbet açık olmalı"
                )
        else:
            await status.edit_text(
                f"✅ **Kuyruğa eklendi! ({source_name})**\n"
                f"🎵 {result['title']}\n"
                f"⏱ {result['duration']}\n"
                f"📋 Sıra: #{position + 1}\n"
                f"👤 {message.from_user.mention}"
            )
    
    except Exception as e:
        await status.edit_text(f"❌ **Hata:** `{str(e)}`")
        import traceback
        traceback.print_exc()
