import requests
import re

# সোর্স ইউআরএলগুলো
urls = [
    "https://raw.githubusercontent.com/srhady/tapmad-bd/refs/heads/main/tapmad_bd.m3u",
    "https://raw.githubusercontent.com/srhady/Fancode-bd/refs/heads/main/main_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/SonyLiv/refs/heads/main/sonyliv_playlist.m3u"
]

def merge_playlists():
    # প্লেলিস্টের শুরু
    merged_content = "#EXTM3U\n"
    
    # আপনার কাস্টম প্রমোশন সেকশন
    PROMOTION = """#EXTINF:-1 tvg-id="" tvg-logo="https://bdixiptvbd.com/logo.png" group-title="IBS TV PROMOTION",--- [ IBS TV PROMOTION ] ---
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,IBS TV Download: bdixiptvbd.com
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,Telegram Channel: https://t.me/bdixiptvbd
https://bdixiptvbd.com/live/Telegram.mp4
#EXTINF:-1,WhatsApp: 01610598422
https://bdixiptvbd.com/live/Telegram.mp4
"""
    merged_content += PROMOTION

    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    line = line.strip()
                    # ১. শুধুমাত্র #EXTINF দিয়ে শুরু হওয়া লাইন অথবা চ্যানেল ইউআরএল (http) গুলো নেওয়া হবে
                    # ২. #EXTM3U বা অন্য কোনো কমেন্ট (# Playlist Name ইত্যাদি) বাদ দেওয়া হবে
                    if line.startswith("#EXTINF") or line.startswith("http"):
                        merged_content += line + "\n"
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # ফাইনাল ফাইল সেভ করা
    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print("Success! Clean playlist generated.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    merge_playlists()
    
