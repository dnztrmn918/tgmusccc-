import asyncio
import logging
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid, FloodWait
from config import Config
from bot.handlers import register_handlers
from bot.core.call import call_manager
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

# Global clients
bot_client = None
user_client = None

async def main():
    global bot_client, user_client
    
    try:
        # Yapılandırmayı doğrula
        Config.validate()
        logger.info("✅ Yapılandırma doğrulandı")
        
        # Bot client'ini oluştur
        bot_client = Client(
            "music_bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )
        
        # User client'ini oluştur (müzik çalmak için gerekli)
        user_client = Client(
            "music_user",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_string=Config.STRING_SESSION
        )
        
        # Handler'ları kaydet
        register_handlers(bot_client)
        logger.info("✅ Handler'lar kaydedildi")
        
        # Bot'u başlat (FloodWait kontrolü ile)
        try:
            await bot_client.start()
            logger.info(f"✅ Bot başlatıldı: @{bot_client.me.username}")
        except FloodWait as e:
            logger.warning(f"⏳ FloodWait: {e.value} saniye bekleniyor...")
            await asyncio.sleep(e.value + 5)
            await bot_client.start()
            logger.info(f"✅ Bot başlatıldı: @{bot_client.me.username}")
        
        # User client'ı başlat
        try:
            await user_client.start()
            logger.info("✅ User client başlatıldı")
        except FloodWait as e:
            logger.warning(f"⏳ FloodWait (user): {e.value} saniye bekleniyor...")
            await asyncio.sleep(e.value + 5)
            await user_client.start()
            logger.info("✅ User client başlatıldı")
        
        # PyTgCalls'u başlat
        await call_manager.init(user_client)
        logger.info("✅ PyTgCalls başlatıldı")
        
        # Bot bilgilerini göster
        me = await bot_client.get_me()
        logger.info(f"♫ Bot Adı: {me.first_name}")
        logger.info(f"♫ Bot Username: @{me.username}")
        logger.info(f"♫ Bot ID: {me.id}")
        
        # Cookie durumunu kontrol et
        cookies_path = os.path.join(os.path.dirname(__file__), '..', 'cookies.txt')
        if os.path.exists(cookies_path):
            logger.info("🍪 Cookie dosyası mevcut - YouTube erişimi geliştirilmiş")
        else:
            logger.warning("⚠️ Cookie dosyası bulunamadı - Bazı videolar çalışmayabilir")
            logger.info("💡 İpucu: cookies.txt dosyasını ana dizine ekleyin")
        
        logger.info("\n♫ Müzik Botu hazır! Komutlar için /start yazın")
        
        # Bot'u aktif tut
        await idle()
        
    except (ApiIdInvalid, AccessTokenInvalid) as e:
        logger.error(f"❌ Geçersiz API bilgileri: {e}")
    except FloodWait as e:
        logger.error(f"❌ FloodWait hatası: {e.value} saniye beklemeniz gerekiyor")
        logger.info(f"⏰ Yaklaşık {e.value // 60} dakika sonra tekrar deneyin")
    except ValueError as e:
        logger.error(f"❌ Yapılandırma hatası: {e}")
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            if bot_client and bot_client.is_connected:
                await bot_client.stop()
        except:
            pass
        try:
            if user_client and user_client.is_connected:
                await user_client.stop()
        except:
            pass
        logger.info("⚠️ Bot durduruldu")

def get_bot_client():
    return bot_client

def get_user_client():
    return user_client

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot kapatılıyor...")
