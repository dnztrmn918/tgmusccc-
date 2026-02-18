import os
import asyncio
from typing import Optional, Dict
from config import Config

class SoundCloudDownloader:
    """SoundCloud indirici - yt-dlp kullanarak"""
    
    def __init__(self):
        pass
    
    def _get_ydl_opts(self, download: bool = False) -> dict:
        """yt-dlp ayarlarını döndür"""
        opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
        }
        
        if download:
            opts['format'] = 'bestaudio/best'
            opts['outtmpl'] = f"{Config.DOWNLOAD_DIR}/sc_%(id)s.%(ext)s"
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        return opts
    
    async def search(self, query: str) -> Optional[Dict]:
        """SoundCloud'da şarkı ara"""
        import yt_dlp
        
        def _search():
            opts = self._get_ydl_opts(download=False)
            
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    # SoundCloud'da ara
                    result = ydl.extract_info(f"scsearch:{query}", download=False)
                    
                    if not result or 'entries' not in result or not result['entries']:
                        return None
                    
                    track = result['entries'][0]
                    if not track:
                        return None
                    
                    # Süreyi formatla
                    duration = track.get('duration', 0) or 0
                    minutes = int(duration) // 60
                    seconds = int(duration) % 60
                    duration_str = f"{minutes:02d}:{seconds:02d}"
                    
                    return {
                        'title': track.get('title', 'Bilinmeyen'),
                        'url': track.get('webpage_url', ''),
                        'track_id': str(track.get('id', '')),
                        'duration': duration_str,
                        'thumbnail': track.get('thumbnail', ''),
                        'source': 'soundcloud'
                    }
            except Exception as e:
                print(f"SoundCloud arama hatası: {e}")
                return None
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _search)
    
    async def download(self, url: str, track_id: str) -> Optional[str]:
        """SoundCloud'dan ses dosyasını indir"""
        import yt_dlp
        
        def _download():
            opts = self._get_ydl_opts(download=True)
            
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    if info:
                        # İndirilen dosya yolunu bul
                        file_path = f"{Config.DOWNLOAD_DIR}/sc_{track_id}.mp3"
                        
                        # mp3 yoksa diğer formatları kontrol et
                        if not os.path.exists(file_path):
                            for ext in ['mp3', 'opus', 'm4a', 'webm']:
                                alt_path = f"{Config.DOWNLOAD_DIR}/sc_{track_id}.{ext}"
                                if os.path.exists(alt_path):
                                    file_path = alt_path
                                    break
                        
                        # Hala bulunamadıysa, indirilen dosyayı bul
                        if not os.path.exists(file_path):
                            for f in os.listdir(Config.DOWNLOAD_DIR):
                                if f.startswith(f"sc_{track_id}"):
                                    file_path = os.path.join(Config.DOWNLOAD_DIR, f)
                                    break
                        
                        if os.path.exists(file_path):
                            print(f"✅ SoundCloud'dan indirildi: {file_path}")
                            return file_path
                    
                    return None
            except Exception as e:
                print(f"SoundCloud indirme hatası: {e}")
                return None
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _download)

# Global instance
sc_downloader = SoundCloudDownloader()

async def search_soundcloud(query: str) -> Optional[Dict]:
    """SoundCloud'da ara"""
    return await sc_downloader.search(query)

async def download_soundcloud_audio(url: str, track_id: str) -> Optional[str]:
    """SoundCloud'dan indir"""
    return await sc_downloader.download(url, track_id)
