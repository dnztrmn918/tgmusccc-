import asyncio
import logging
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid
from config import Config
from bot.handlers import register_handlers
import os

# Logging yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Download dizinini oluştur
if not os.path.exists(Config.DOWNLOAD_DIR):
    os.makedirs(Config.DOWNLOAD_DIR)

async def main():
    try:
        # Yapılandırmayı doğrula
        Config.validate()
        logger.info("✅ Yapılandırma doğrulandı")
        
        # Bot client'ini oluştur
        app = Client(
            "music_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )
        
        # User client'ini oluştur (müzik çalmak için gerekli)
        user = Client(
            "music_user",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_string=Config.STRING_SESSION
        )
        
        # Handler'ları kaydet
        register_handlers(app)
        logger.info("✅ Handler'lar kaydedildi")
        
        # Bot'u başlat
        await app.start()
        logger.info(f"✅ Bot başlatıldı: @{app.me.username}")
        
        # User client'ı başlat
        await user.start()
        logger.info("✅ User client başlatıldı")
        
        # Bot bilgilerini göster
        me = await app.get_me()
        logger.info(f"♫ Bot Adı: {me.first_name}")
        logger.info(f"♫ Bot Username: @{me.username}")
        logger.info(f"♫ Bot ID: {me.id}")
        logger.info("\n♫ Müzik Botu hazır! Komutlar için /start yazın")
        
        # Bot'u aktif tut
        await idle()
        
    except (ApiIdInvalid, AccessTokenInvalid) as e:
        logger.error(f"❌ Geçersiz API bilgileri: {e}")
    except ValueError as e:
        logger.error(f"❌ Yapılandırma hatası: {e}")
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
    finally:
        if 'app' in locals():
            await app.stop()
        if 'user' in locals():
            await user.stop()
        logger.info("⚠️ Bot durduruldu")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot kapatiliyor...")
