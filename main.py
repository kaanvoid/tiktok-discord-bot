import requests
import time
from datetime import datetime

# ╔════════════════════════════════════════════════╗
# ║                AYARLAR                         ║
# ╚════════════════════════════════════════════════╝

TIKTOK_USERNAME = "ll.sude_0"  # TikTok kullanıcı adın
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1438467806676123762/9hnoLANTANvNrz4OqoxGb5NybQpQAznjRxv_IUrZIMzjbXZLhfeBStyD5uMWqpg7goyH"  # Discord webhook bağlantın
CHECK_INTERVAL = 60  # saniye cinsinden kontrol süresi (60 = 1 dakika)

# ╔════════════════════════════════════════════════╗
# ║          DİSCORD MESAJ GÖNDERME FONKSİYONU     ║
# ╚════════════════════════════════════════════════╝

def send_discord_embed(title, description, color=0xFF69B4):
    """Discord'a embed şeklinde mesaj gönderir."""
    payload = {
        "content": "@everyone",  # buraya @here da yazabilirsin
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "TikTok Canlı Yayın Bildirimi 💫"
                }
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code in (200, 204):
            print("✅ Discord’a mesaj gönderildi.")
        else:
            print(f"⚠️ Discord hatası ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"⚠️ Discord’a mesaj gönderilemedi: {e}")

# ╔════════════════════════════════════════════════╗
# ║          TIKTOK CANLI DURUMU KONTROLÜ          ║
# ╚════════════════════════════════════════════════╝

def is_live(username):
    """TikTok kullanıcısının yayında olup olmadığını kontrol eder."""
    try:
        url = f"https://www.tiktok.com/@{username}/live"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) "
                "Gecko/20100101 Firefox/122.0"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        response = requests.get(url, headers=headers, timeout=10)
        # "isLive":true veya "LIVE_NOW" yazısı yayında olduğunu gösterir
        return ('"isLive":true' in response.text) or ("LIVE_NOW" in response.text)

    except Exception as e:
        print(f"⚠️ TikTok kontrol hatası: {e}")
        return False

# ╔════════════════════════════════════════════════╗
# ║                 ANA DÖNGÜ                      ║
# ╚════════════════════════════════════════════════╝

def main():
    print("🚀 TikTok Canlı Yayın Bildirim Botu Başlatıldı!")
    print(f"🔍 @{TIKTOK_USERNAME} kullanıcısı takip ediliyor...\n")
    was_live = False

    while True:
        live_now = is_live(TIKTOK_USERNAME)

        if live_now and not was_live:
            print("🎥 Yayın başladı!")
            send_discord_embed(
                title=f"🎬 {TIKTOK_USERNAME.upper()} CANLI YAYINDA!",
                description=f"🔗 [Canlı yayına gitmek için tıkla](https://www.tiktok.com/@{TIKTOK_USERNAME}/live)"
            )
            was_live = True

        elif not live_now and was_live:
            print("📴 Yayın sona erdi.")
            send_discord_embed(
                title=f"📴 {TIKTOK_USERNAME.upper()} yayını kapattı.",
                description="Canlı yayın sona erdi. Yeni yayınları kaçırmamak için takipte kal 💫",
                color=0x808080
            )
            was_live = False

        else:
            status = "🟢 CANLI" if live_now else "⚪️ ÇEVRİMDIŞI"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Durum: {status}")

        time.sleep(CHECK_INTERVAL)

# ╔════════════════════════════════════════════════╗
# ║                ÇALIŞTIRMA                      ║
# ╚════════════════════════════════════════════════╝

if __name__ == "__main__":
    main()
