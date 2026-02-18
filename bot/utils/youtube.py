import aiohttp
import asyncio
from typing import Optional, Dict
import os
from config import Config

# Invidious public instances
INVIDIOUS_INSTANCES = [
    "https://inv.nadeko.net",
    "https://invidious.privacydev.net",
    "https://iv.melmac.space",
]

class YouTubeDownloader:
    def __init__(self):
        self.session = None
        self.current_instance = 0
    
    async def get_session(self):
        """Aiohttp session oluştur"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def get_instance(self):
        """Invidious instance al"""
        instance = INVIDIOUS_INSTANCES[self.current_instance]
        self.current_instance = (self.current_instance + 1) % len(INVIDIOUS_INSTANCES)
        return instance
    
    async def search(self, query: str) -> Optional[Dict]:
        """Invidious API ile YouTube'da şarkı ara"""
        
        # Tüm instancelari dene
        for instance in INVIDIOUS_INSTANCES:
            try:
                session = await self.get_session()
                
                url = f"{instance}/api/v1/search"
                params = {
                    'q': query,
                    'type': 'video',
                    'sort_by': 'relevance'
                }
                
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status != 200:
                        print(f"{instance} yanıt vermedi, sonrakini deniyor...")
                        continue
                    
                    data = await response.json()
                    
                    if not data or len(data) == 0:
                        continue
                    
                    video = data[0]
                    
                    # Süreyi dönüştür
                    duration = int(video.get('lengthSeconds', 0))
                    minutes = duration // 60
                    seconds = duration % 60
                    duration_str = f"{minutes:02d}:{seconds:02d}"
                    
                    print(f"✅ {instance} ile bulundu!")
                    
                    return {
                        'title': video.get('title', 'Bilinmeyen'),
                        'url': f"https://youtube.com/watch?v={video['videoId']}",
                        'video_id': video.get('videoId', ''),
                        'duration': duration_str,
                        'thumbnail': video.get('videoThumbnails', [{}])[0].get('url', ''),
                    }
            
            except Exception as e:
                print(f"Invidious arama hatası ({instance}): {e}")
                continue
        
        # Hiçbir instance çalışmadı
        return None
    
    async def download(self, video_id: str) -> Optional[str]:
        """Invidious API ile ses dosyasını indir"""
        
        # Tüm instancelari dene
        for instance in INVIDIOUS_INSTANCES:
            try:
                session = await self.get_session()
                
                # Video bilgilerini al
                url = f"{instance}/api/v1/videos/{video_id}"
                
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        print(f"{instance} video bilgisi alınamadı, sonrakini deniyor...")
                        continue
                    
                    data = await response.json()
                    
                    # En iyi ses formatını bul
                    audio_formats = [f for f in data.get('adaptiveFormats', []) 
                                   if f.get('type', '').startswith('audio')]
                    
                    if not audio_formats:
                        continue
                    
                    # En yüksek kaliteli ses formatını seç
                    audio_format = max(audio_formats, key=lambda x: x.get('bitrate', 0))
                    audio_url = audio_format.get('url')
                    
                    if not audio_url:
                        continue
                    
                    # Ses dosyasını indir
                    download_path = f"{Config.DOWNLOAD_DIR}/{video_id}.mp3"
                    
                    async with session.get(audio_url, timeout=60) as audio_response:
                        if audio_response.status != 200:
                            continue
                        
                        # Dosyayı kaydet
                        with open(download_path, 'wb') as f:
                            while True:
                                chunk = await audio_response.content.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                    
                    if os.path.exists(download_path):
                        print(f"✅ {instance} ile indirildi!")
                        return download_path
            
            except Exception as e:
                print(f"Invidious indirme hatası ({instance}): {e}")
                continue
        
        # Hiçbir instance çalışmadı
        return None
    
    async def close(self):
        """Session'ı kapat"""
        if self.session:
            await self.session.close()

# Global instance
downloader = YouTubeDownloader()

async def search_youtube(query: str) -> Optional[Dict]:
    """YouTube'da ara"""
    return await downloader.search(query)

async def download_audio(video_id: str) -> Optional[str]:
    """Ses dosyasını indir"""
    return await downloader.download(video_id)
