import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Ayarları
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    STRING_SESSION = os.getenv("STRING_SESSION", "")
    
    # Bot Sahibi
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    
    # Log Kanalı (Opsiyonel)
    LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))
    
    # Müzik Ayarları
    DOWNLOAD_DIR = "downloads"
    MAX_QUEUE_SIZE = 50
    
    # Destek
    SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "")
    SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "")
    
    @staticmethod
    def validate():
        """Gerekli yapılandırmaları kontrol et"""
        required = {
            "API_ID": Config.API_ID,
            "API_HASH": Config.API_HASH,
            "BOT_TOKEN": Config.BOT_TOKEN,
            "STRING_SESSION": Config.STRING_SESSION,
        }
        
        missing = [key for key, value in required.items() if not value or value == "0"]
        
        if missing:
            raise ValueError(f"Eksik yapılandırma: {', '.join(missing)}")
        
        return True
