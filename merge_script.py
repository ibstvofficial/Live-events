import requests

# আপনার সোর্স ইউআরএলগুলো
urls = [
    "https://raw.githubusercontent.com/srhady/tapmad-bd/refs/heads/main/tapmad_bd.m3u",
    "https://raw.githubusercontent.com/srhady/Fancode-bd/refs/heads/main/main_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/SonyLiv/refs/heads/main/sonyliv_playlist.m3u"
]

def merge_playlists():
    # প্লেলিস্টের শুরু
    merged_content = "#EXTM3U\n"
    
    # আপনার দেওয়া প্রমোশন সেকশন (সবার উপরে শো করবে)
    # এখানে ট্রিপল কোটেশন ব্যবহার করা হয়েছে যাতে এরর না আসে
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

    # চ্যানেলগুলো অন্য প্লেলিস্ট থেকে যোগ করা
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                content = response.text.strip()
                if content:
                    lines = content.splitlines()
                    # যদি ফাইলটি #EXTM3U দিয়ে শুরু হয়, তবে প্রথম লাইন বাদ দিয়ে বাকিটুকু নেওয়া হবে
                    if lines and lines[0].startswith("#EXTM3U"):
                        merged_content += "\n".join(lines[1:]) + "\n"
                    else:
                        merged_content += content + "\n"
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # ফাইনাল প্লেলিস্ট ফাইল (playlist.m3u) সেভ করা
    try:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print("Success! All playlists merged with your promotion info.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    merge_playlists()
  
