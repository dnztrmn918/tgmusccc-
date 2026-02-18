# 🎵 Telegram Müzik Botu

YouTube ve SoundCloud üzerinden müzik çalan Telegram botu.

## ✨ Özellikler

- 🎵 YouTube'dan müzik arama ve çalma
- 📋 Müzik kuyruğu sistemi
- ⏯ Oynatma kontrolleri (pause, resume, stop)
- 🔊 Yüksek kaliteli ses
- 👥 Grup sesli sohbetlerinde çalışır
- 🚀 Kolay kurulum

## 📋 Gereksinimler

- Python 3.11+
- FFmpeg
- Telegram Bot Token
- Telegram API ID & Hash
- String Session

## 🚀 Kurulum

### 1. Gerekli API Anahtarlarını Alın

#### a) API_ID ve API_HASH
1. https://my.telegram.org adresine gidin
2. Telefon numaranızla giriş yapın
3. "API Development Tools" bölümüne gidin
4. Yeni bir uygulama oluşturun
5. `API_ID` ve `API_HASH` değerlerini kopyalayın

#### b) BOT_TOKEN
1. Telegram'da @BotFather botunu açın
2. `/newbot` komutunu gönderin
3. Bot için isim ve username belirleyin
4. Bot token'ınızı kopyalayın

#### c) STRING_SESSION
1. @StringFatherBot veya @SessionGenBot botlarından birini açın
2. Bot'un talimatlarını takip edin
3. Telefon numaranızı ve OTP kodunu girin
4. String session'ınızı kopyalayın

### 2. Projeyi Klonlayın

```bash
git clone https://github.com/kullanici_adi/telegram-music-bot.git
cd telegram-music-bot
```

### 3. Sanal Ortam Oluşturun (Opsiyonel)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 4. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 5. FFmpeg Kurun

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg -y
```

#### Windows:
1. https://ffmpeg.org/download.html adresinden indirin
2. PATH'e ekleyin

#### macOS:
```bash
brew install ffmpeg
```

### 6. Yapılandırma

`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
cp .env.example .env
nano .env
```

Aşağıdaki değerleri doldurun:

```env
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
STRING_SESSION=your_string_session_here
OWNER_ID=123456789
LOG_GROUP_ID=-1001234567890
SUPPORT_GROUP=https://t.me/your_support_group
SUPPORT_CHANNEL=https://t.me/your_channel
```

### 7. Botu Başlatın

```bash
python3 -m bot
```

## 📦 Koyeb'de Deploy

### 1. GitHub'a Push

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Koyeb'de Deploy

1. https://app.koyeb.com adresine gidin
2. "Create App" butonuna tıklayın
3. GitHub repository'nizi seçin
4. Build yapılandırması:
   - **Builder:** Buildpack
   - **Build command:** (boş bırakın)
   - **Run command:** (boş bırakın, Procfile kullanılacak)
5. Environment Variables ekleyin:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `STRING_SESSION`
   - `OWNER_ID`
   - (Diğer opsiyonel değişkenler)
6. "Deploy" butonuna tıklayın

## 🎯 Komutlar

| Komut | Açıklama |
|-------|----------|
| `/start` | Botu başlat ve yardım mesajını göster |
| `/play <şarkı adı>` | YouTube'dan şarkı ara ve çal |
| `/pause` | Müziği duraklat |
| `/resume` | Müziğe devam et |
| `/stop` | Müziği durdur ve sesli sohbetten ayrıl |
| `/queue` | Mevcut müzik kuyruğunu göster |

## 💡 Kullanım

1. Botu grubunuza ekleyin
2. Botu yönetici yapın (sesli sohbet izinleriyle)
3. Sesli sohbete katılın
4. Grupta `/play Tarkan Şımarık` gibi bir komut gönderin
5. Bot şarkıyı bulup çalmaya başlayacak

## 🛠 Teknik Detaylar

### Kullanılan Teknolojiler

- **Pyrogram:** Telegram MTProto API
- **py-tgcalls:** Sesli sohbet entegrasyonu
- **yt-dlp:** YouTube indirme
- **FFmpeg:** Ses işleme
- **aiohttp:** Asenkron HTTP istekleri

### Proje Yapısı

```
telegram-music-bot/
├── bot/
│   ├── __init__.py
│   ├── __main__.py          # Ana bot dosyası
│   ├── handlers/            # Komut işleyicileri
│   │   ├── __init__.py
│   │   ├── start.py         # /start komutu
│   │   ├── play.py          # /play komutu
│   │   ├── controls.py      # pause/resume/stop
│   │   └── queue.py         # /queue komutu
│   └── utils/               # Yardımcı fonksiyonlar
│       ├── __init__.py
│       ├── youtube.py       # YouTube işlemleri
│       ├── soundcloud.py    # SoundCloud (gelecek)
│       └── queue_manager.py # Kuyruk yönetimi
├── downloads/               # İndirilen dosyalar (otomatik oluşur)
├── config.py                # Yapılandırma
├── requirements.txt         # Python bağımlılıkları
├── Procfile                 # Koyeb/Heroku yapılandırması
├── runtime.txt              # Python sürümü
├── .env                     # Ortam değişkenleri (gizli)
├── .env.example             # Ortam değişkenleri şablonu
├── .gitignore               # Git ignore dosyası
└── README.md                # Bu dosya
```

## ⚠️ Notlar

- Bot şu anda YouTube desteği ile çalışıyor
- SoundCloud desteği gelecek sürümlerde eklenecek
- py-tgcalls entegrasyonu için ek yapılandırma gerekebilir
- Bot'un sesli sohbete katılabilmesi için yönetici olması gerekir

## 🐛 Sorun Giderme

### Bot çalışmıyor
- API anahtarlarınızı kontrol edin
- `.env` dosyasının doğru yapılandırıldığından emin olun
- `python3 -m bot` ile çalıştırdığınızdan emin olun

### Müzik çalmıyor
- Bot'un sesli sohbet izinleri olduğundan emin olun
- FFmpeg'in kurulu olduğunu kontrol edin: `ffmpeg -version`
- String session'ınızın geçerli olduğundan emin olun

### İndirme hataları
- İnternet bağlantınızı kontrol edin
- yt-dlp güncel mi kontrol edin: `pip install -U yt-dlp`

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Bu repo'yu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 💬 Destek

Sorunlarınız için GitHub Issues kullanabilirsiniz.

## 🌟 Teşekkürler

- [Pyrogram](https://docs.pyrogram.org/)
- [py-tgcalls](https://github.com/pytgcalls/pytgcalls)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!
