import asyncio
from typing import Dict, Optional
from pytgcalls import PyTgCalls, filters
from pytgcalls.types import MediaStream, AudioQuality
from pyrogram import Client
import os

class CallManager:
    """Sesli sohbet yöneticisi - py-tgcalls entegrasyonu"""
    
    def __init__(self):
        self.call: Optional[PyTgCalls] = None
        self.user_client: Optional[Client] = None
        self.active_calls: Dict[int, bool] = {}  # chat_id: is_playing
        self.paused: Dict[int, bool] = {}  # chat_id: is_paused
    
    async def init(self, user_client: Client):
        """PyTgCalls'u başlat"""
        self.user_client = user_client
        self.call = PyTgCalls(user_client)
        
        # Event handler'ları kaydet
        @self.call.on_update(filters.stream_end)
        async def on_stream_end(client, update):
            chat_id = update.chat_id
            print(f"🎵 Stream bitti: {chat_id}")
            self.active_calls[chat_id] = False
            # Kuyruktan sonraki şarkıyı çal
            from bot.utils.queue_manager import queue_manager
            next_song = queue_manager.skip_song(chat_id)
            if next_song:
                await self.play(chat_id, next_song['file_path'])
        
        await self.call.start()
        print("✅ PyTgCalls başlatıldı")
    
    async def play(self, chat_id: int, file_path: str) -> bool:
        """Sesli sohbette müzik çal"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Dosya bulunamadı: {file_path}")
                return False
            
            # Zaten aktif bir çağrı varsa, stream'i değiştir
            if chat_id in self.active_calls and self.active_calls[chat_id]:
                await self.call.play(
                    chat_id,
                    MediaStream(
                        file_path,
                        audio_parameters=AudioQuality.STUDIO
                    )
                )
            else:
                # Yeni çağrı başlat
                await self.call.play(
                    chat_id,
                    MediaStream(
                        file_path,
                        audio_parameters=AudioQuality.STUDIO
                    )
                )
            
            self.active_calls[chat_id] = True
            self.paused[chat_id] = False
            print(f"▶️ Çalınıyor: {file_path} -> {chat_id}")
            return True
            
        except Exception as e:
            print(f"❌ Çalma hatası: {e}")
            return False
    
    async def pause(self, chat_id: int) -> bool:
        """Müziği duraklat"""
        try:
            if chat_id in self.active_calls and self.active_calls[chat_id]:
                await self.call.pause_stream(chat_id)
                self.paused[chat_id] = True
                print(f"⏸ Duraklatıldı: {chat_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ Duraklatma hatası: {e}")
            return False
    
    async def resume(self, chat_id: int) -> bool:
        """Müziğe devam et"""
        try:
            if chat_id in self.paused and self.paused[chat_id]:
                await self.call.resume_stream(chat_id)
                self.paused[chat_id] = False
                print(f"▶️ Devam ediyor: {chat_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ Devam hatası: {e}")
            return False
    
    async def stop(self, chat_id: int) -> bool:
        """Müziği durdur ve sesli sohbetten ayrıl"""
        try:
            if chat_id in self.active_calls:
                await self.call.leave_call(chat_id)
                self.active_calls[chat_id] = False
                self.paused[chat_id] = False
                print(f"⏹ Durduruldu ve ayrıldı: {chat_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ Durdurma hatası: {e}")
            return False
    
    def is_playing(self, chat_id: int) -> bool:
        """Müzik çalıyor mu?"""
        return self.active_calls.get(chat_id, False) and not self.paused.get(chat_id, False)
    
    def is_paused(self, chat_id: int) -> bool:
        """Müzik duraklatılmış mı?"""
        return self.paused.get(chat_id, False)

# Global instance
call_manager = CallManager()
