import yt_dlp
import asyncio
from typing import Optional, Dict
import os
from config import Config

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{Config.DOWNLOAD_DIR}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_color': True,
            'age_limit': None,
            'geo_bypass': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],
                    'player_skip': ['js', 'configs', 'webpage'],
                    'player_client': ['android', 'web'],
                }
            },
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    
    async def search(self, query: str) -> Optional[Dict]:
        """YouTube'da şarkı ara"""
        try:
            search_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'default_search': 'ytsearch1',
                'nocheckcertificate': True,
                'geo_bypass': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                    }
                },
            }
            
            with yt_dlp.YoutubeDL(search_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, f"ytsearch1:{query}", download=False)
                
                if not info or 'entries' not in info or not info['entries']:
                    return None
                
                video = info['entries'][0]
                
                # Süreyi dönüştür
                duration = int(video.get('duration', 0))  # Float'u int'e çevir
                minutes = duration // 60
                seconds = duration % 60
                duration_str = f"{minutes:02d}:{seconds:02d}"
                
                return {
                    'title': video.get('title', 'Bilinmeyen'),
                    'url': f"https://youtube.com/watch?v={video['id']}",
                    'duration': duration_str,
                    'thumbnail': video.get('thumbnail', ''),
                    'id': video.get('id', ''),
                }
        
        except Exception as e:
            print(f"YouTube arama hatası: {e}")
            return None
    
    async def download(self, url: str) -> Optional[str]:
        """Şarkıyı indir"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, url, download=True)
                
                # İndirilen dosya yolunu bul
                file_path = ydl.prepare_filename(info)
                # Uzantıyı mp3 olarak değiştir
                file_path = os.path.splitext(file_path)[0] + '.mp3'
                
                if os.path.exists(file_path):
                    return file_path
                
                return None
        
        except Exception as e:
            print(f"YouTube indirme hatası: {e}")
            return None

# Global instance
downloader = YouTubeDownloader()

async def search_youtube(query: str) -> Optional[Dict]:
    """YouTube'da ara"""
    return await downloader.search(query)

async def download_audio(url: str) -> Optional[str]:
    """Ses dosyasını indir"""
    return await downloader.download(url)
