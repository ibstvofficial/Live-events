import requests
import datetime
import os

# আপনার সোর্স লিঙ্কগুলো
urls = [
    "https://raw.githubusercontent.com/srhady/SonyLiv/refs/heads/main/sonyliv_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/Fancode-bd/refs/heads/main/main_playlist.m3u",
    "https://raw.githubusercontent.com/srhady/join_telegram_chennal-livesportsplay/refs/heads/main/bangla.m3u"
]

# ব্যাকআপ লিঙ্ক এবং প্রমোশন তথ্য
BACKUP_VIDEO = "https://bdixiptvbd.com/live/Telegram.mp4"

PROMOTION = (
    "#EXTINF:-1 tvg-id=\"\" tvg-logo=\"https://bdixiptvbd.com/logo.png\" group-title=\"IBS TV PROMOTION\",--- [ IBS TV PROMOTION ] ---\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
    "#EXTINF:-1,IBS TV Download: bdixiptvbd.com\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
    "#EXTINF:-1,Telegram Channel: https://t.me/bdixiptvbd\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
    "#EXTINF:-1,WhatsApp: 01610598422\n"
    "https://bdixiptvbd.com/live/Telegram.mp4\n"
)

def process_m3u(text):
    processed_lines = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#EXTM3U") or line.startswith("##"):
            i += 1
            continue
            
        if line.startswith("#EXTINF"):
            info_line = line
            url_line = BACKUP_VIDEO # ডিফল্ট ব্যাকআপ
            
            # পরবর্তী লাইন চেক করা (লিঙ্ক এর জন্য)
            if i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if next_line and not next_line.startswith("#"):
                    url_line = next_line
                    i += 1 # লিঙ্ক পাওয়া গেছে
            
            processed_lines.append(info_line)
            processed_lines.append(url_line)
        i += 1
    return "\n".join(processed_lines)

def main():
    print("Update process started...")
    header = "#EXTM3U\n"
    header += f"## Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    header += "## IBS TV: bdixiptvbd.com\n\n"
    
    final_content = header + PROMOTION + "\n"

    for url in urls:
        try:
            print(f"Fetching: {url}")
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                data = process_m3u(r.text)
                final_content += f"## Source: {url}\n" + data + "\n\n"
            else:
                print(f"Failed to load: {url}")
        except Exception as e:
            print(f"Error: {e}")

    # ফাইল সেভ করা
    with open("merged_playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_content.strip())
    print("Task completed: merged_playlist.m3u created.")

if __name__ == "__main__":
    main()


