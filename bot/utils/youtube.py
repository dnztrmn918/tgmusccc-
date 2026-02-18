import os
import asyncio
from typing import Optional, Dict
from config import Config

class YouTubeDownloader:
    """YouTube indirici - yt-dlp + cookie desteği"""
    
    def __init__(self):
        self.cookies_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cookies.txt')
        self.last_error = None
    
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
            'extract_flat': not download,
        }
        
        # Cookie dosyası varsa ekle
        if os.path.exists(self.cookies_file):
            opts['cookiefile'] = self.cookies_file
            print(f"✅ Cookie dosyası yüklendi: {self.cookies_file}")
        else:
            # Cookie olmadan alternatif ayarlar
            opts['extractor_args'] = {'youtube': {'player_client': ['android', 'web']}}
        
        if download:
            opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
            opts['outtmpl'] = f"{Config.DOWNLOAD_DIR}/%(id)s.%(ext)s"
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        
        return opts
    
    async def search(self, query: str) -> Optional[Dict]:
        """YouTube'da şarkı ara"""
        import yt_dlp
        
        def _search():
            opts = self._get_ydl_opts(download=False)
            opts['default_search'] = 'ytsearch'
            opts['extract_flat'] = True
            
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    result = ydl.extract_info(f"ytsearch:{query}", download=False)
                    
                    if not result or 'entries' not in result or not result['entries']:
                        return None
                    
                    video = result['entries'][0]
                    if not video:
                        return None
                    
                    # Süreyi formatla
                    duration = video.get('duration', 0) or 0
                    minutes = int(duration) // 60
                    seconds = int(duration) % 60
                    duration_str = f"{minutes:02d}:{seconds:02d}"
                    
                    return {
                        'title': video.get('title', 'Bilinmeyen'),
                        'url': video.get('url') or f"https://youtube.com/watch?v={video.get('id')}",
                        'video_id': video.get('id', ''),
                        'duration': duration_str,
                        'thumbnail': video.get('thumbnail', ''),
                        'source': 'youtube'
                    }
            except Exception as e:
                self.last_error = str(e)
                print(f"YouTube arama hatası: {e}")
                return None
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _search)
    
    async def download(self, video_id: str) -> Optional[str]:
        """YouTube'dan ses dosyasını indir"""
        import yt_dlp
        
        def _download():
            opts = self._get_ydl_opts(download=True)
            url = f"https://youtube.com/watch?v={video_id}"
            
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    if info:
                        # İndirilen dosya yolunu bul
                        file_path = f"{Config.DOWNLOAD_DIR}/{video_id}.mp3"
                        
                        # mp3 yoksa diğer formatları kontrol et
                        if not os.path.exists(file_path):
                            for ext in ['m4a', 'webm', 'opus']:
                                alt_path = f"{Config.DOWNLOAD_DIR}/{video_id}.{ext}"
                                if os.path.exists(alt_path):
                                    file_path = alt_path
                                    break
                        
                        if os.path.exists(file_path):
                            self.last_error = None
                            print(f"✅ YouTube'dan indirildi: {file_path}")
                            return file_path
                    
                    return None
            except Exception as e:
                self.last_error = str(e)
                print(f"YouTube indirme hatası: {e}")
                return None
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _download)
    
    def is_cookie_error(self) -> bool:
        """Son hata cookie ile ilgili mi?"""
        if not self.last_error:
            return False
        error_lower = self.last_error.lower()
        cookie_keywords = ['sign in', 'cookie', 'login', 'age', 'restricted', 'bot', 'captcha', 'verify']
        return any(kw in error_lower for kw in cookie_keywords)

# Global instance
downloader = YouTubeDownloader()

async def search_youtube(query: str) -> Optional[Dict]:
    """YouTube'da ara"""
    return await downloader.search(query)

async def download_audio(video_id: str) -> Optional[str]:
    """YouTube'dan indir"""
    return await downloader.download(video_id)

def is_youtube_cookie_error() -> bool:
    """Cookie hatası mı?"""
    return downloader.is_cookie_error()
