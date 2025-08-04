import requests
import time
import json
import os

data_dir = "data"
json_filename = os.path.join(data_dir, "top_characters.json")
js_filename = os.path.join(data_dir, "top_characters.min.js")
compact_json_filename = os.path.join(data_dir, "top_characters.compact.json")
compact_js_filename = os.path.join(data_dir, "top_characters.compact.min.js")

all_characters = []
compact_characters = []

page = 1
while True:
    url = f"https://api.jikan.moe/v4/top/characters?page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        characters = response.json().get("data", [])
        filtered = [char for char in characters if char.get("favorites", 0) >= 100]

        if not filtered:
            break

        for character in filtered:
            all_characters.append({
                "mal_id": character["mal_id"],
                "favorites": character["favorites"]
            })
            compact_characters.append([
                character["mal_id"],
                character["favorites"]
            ])

        print(f"Page {page} processed.")
        page += 1
        time.sleep(1)
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")
        break

# Write readable JSON
with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(all_characters, f, indent=2, ensure_ascii=False)

# Write minified JS version of readable JSON
with open(js_filename, "w", encoding="utf-8") as f:
    json.dump(all_characters, f, separators=(",", ":"), ensure_ascii=False)

# Write readable compact JSON (array of int pairs)
with open(compact_json_filename, "w", encoding="utf-8") as f:
    json.dump(compact_characters, f, indent=2, ensure_ascii=False)

# Write compact minified JS version
with open(compact_js_filename, "w", encoding="utf-8") as f:
    json.dump(compact_characters, f, separators=(",", ":"), ensure_ascii=False)

print("Files generated:")
print(f"- {json_filename}")
print(f"- {js_filename}")
print(f"- {compact_json_filename}")
print(f"- {compact_js_filename}")
