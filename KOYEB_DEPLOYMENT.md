# 🚀 Koyeb Deployment Rehberi

## Adım Adım Koyeb'de Run Command Ekleme

### 1️⃣ Koyeb Dashboard'a Gidin
- https://app.koyeb.com
- Oluşturduğunuz service'i bulun

### 2️⃣ Service'i Düzenleyin
- Service adına tıklayın
- Sağ üstteki **"Settings"** (⚙️) butonuna tıklayın

### 3️⃣ Builder Ayarlarını Yapın

**Build Command:**
```bash
pip install -r requirements.txt
```
(Boş da bırakabilirsiniz, otomatik algılanır)

**Run Command:**
```bash
python3 -m bot
```
⚠️ Bu komut ÇOK ÖNEMLİ! Mutlaka girin.

### 4️⃣ Environment Variables (Gerekli!)

Aşağıdaki değişkenleri ekleyin:

| Key | Value | Nereden Alınır |
|-----|-------|----------------|
| API_ID | `12345678` | https://my.telegram.org |
| API_HASH | `your_hash_here` | https://my.telegram.org |
| BOT_TOKEN | `123:ABC...` | @BotFather |
| STRING_SESSION | `1BVt...` | @StringFatherBot |
| OWNER_ID | `123456789` | Telegram User ID'niz |

**Opsiyonel:**
- LOG_GROUP_ID
- SUPPORT_GROUP
- SUPPORT_CHANNEL

### 5️⃣ Deploy!
- **"Deploy"** butonuna basın
- Deployment başlayacak (2-3 dakika sürer)

### 6️⃣ Logları Kontrol Edin
- "Logs" sekmesinden şunu görmelisiniz:
```
✅ Yapılandırma doğrulandı
✅ Bot başlatıldı: @YourBotUsername
✅ User client başlatıldı
♫ Müzik Botu hazır! Komutlar için /start yazın
```

## 🔍 Sorun Giderme

### "Can't open file main.py" hatası
➡️ Run command'ı kontrol edin: `python3 -m bot`

### "Invalid API credentials" hatası
➡️ API_ID, API_HASH, BOT_TOKEN'ı kontrol edin

### "String session expired" hatası
➡️ Yeni string session oluşturun: @StringFatherBot

### Bot başlamıyor
➡️ Environment variables'ın hepsinin doğru girildiğinden emin olun

## ✅ Başarılı Deployment Sonrası

1. Bot'u grubunuza ekleyin
2. Bot'u **yönetici** yapın
3. Sesli sohbete katılın
4. `/play tarkan şımarık` yazın
5. Keyfini çıkarın! 🎵
