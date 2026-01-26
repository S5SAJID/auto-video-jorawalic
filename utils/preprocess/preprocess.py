import json
import os
from PIL import Image

def process_gifs_to_frames(json_file_path, base_gif_dir, output_frames_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)

    # Load existing index.json
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    updated_data = []

    for entry in data:
        # Construct the local path to the GIF based on slug or filename
        # This assumes your gifs are named after their slugs or you can match them
        gif_filename = f"{entry['slug']}.gif"
        
        # Search recursively for the GIF in subfolders (angry, happy, etc.)
        gif_path = None
        for root, dirs, files in os.walk(base_gif_dir):
            if gif_filename in files:
                gif_path = os.path.join(root, gif_filename)
                break
        
        if gif_path and os.path.exists(gif_path):
            try:
                with Image.open(gif_path) as img:
                    # Get middle frame index
                    num_frames = getattr(img, 'n_frames', 1)
                    middle_frame_idx = num_frames // 2
                    
                    # Seek to middle frame and save as JPG
                    img.seek(middle_frame_idx)
                    frame_filename = f"{entry['slug']}_middle.jpg"
                    frame_save_path = os.path.join(output_frames_dir, frame_filename)
                    
                    # Convert to RGB to ensure it can be saved as JPG
                    img.convert("RGB").save(frame_save_path, "JPEG")
                    
                    # Update the entry with new fields
                    entry['middleframe'] = frame_save_path
                    entry['description'] = "" # Placeholder for AI description later
                    print(f"✅ Processed: {entry['slug']}")
            except Exception as e:
                print(f"❌ Error processing {gif_path}: {e}")
        else:
            print(f"⚠️ GIF not found for slug: {entry['slug']}")
            entry['middleframe'] = None
            entry['description'] = "File not found"

        updated_data.append(entry)

    # Save the updated index.json
    with open(json_file_path, 'w') as f:
        json.dump(updated_data, f, indent=2)
    
    print(f"\n🚀 Success! index.json updated and frames saved to {output_frames_dir}")

# --- Example Usage in Colab ---
# Assuming your folders are structured exactly as you showed
process_gifs_to_frames('data\\assets\\gifs\\index.json', 'data\\assets\\gifs', 'data\\assets\\middleframes')
