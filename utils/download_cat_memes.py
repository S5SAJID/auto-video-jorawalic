import json
import os
import requests
from lib.gifs_finder import find_gifs

expressions_or_emotions = [
  "happy",
  "angry",
  "sad",
  "confused",
  "hacker",
  "doctor",
  "suspicious",
  "surprised",
  "sleepy",
  "hungry",
  "dancing",
  "judging",
  "crying",
  "scared",
  "cool",
  "robber",
  "engineer",
  "teacher",
  "firefighter",
  "chef",
  "pilot",
  "astronaut",
]

def download_cat_memes():
    index_file = "data/assets/gifs/index.json"
    index_data = []

    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            try:
                index_data = json.load(f)
            except json.JSONDecodeError:
                pass

    # Create a set of existing slugs for O(1) lookup speed
    downloaded_slugs = {item['slug'] for item in index_data}

    for expression in expressions_or_emotions:
        print("CURRENT EXPRESSION :", expression)
        cat_gifs = find_gifs(f"popular {expression} cat meme")
        
        if not cat_gifs:
            continue

        directory = f"data/assets/gifs/{expression}"
        os.makedirs(directory, exist_ok=True)
        
        for gif in cat_gifs:
            slug = gif['slug']
            
            # Check if slug has already been processed in this session or previous ones
            if slug in downloaded_slugs:
                print(f"Skipping already downloaded slug: {slug}")
                continue

            print("CURRENT GIF : ", gif['title'])
            file_path = f"{directory}/{slug}.gif"
            
            try:
                response = requests.get(gif['url'])
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                # Add to index and update our tracking set
                index_data.append({
                    "slug": slug,
                    "url": gif['url'],
                    "expression": expression
                })
                downloaded_slugs.add(slug)

            except Exception as e:
                print(f"Failed to download {gif['url']}: {e}")
                continue

        # Save index after each expression to prevent data loss
        with open(index_file, "w") as f:
            json.dump(index_data, f, indent=2)