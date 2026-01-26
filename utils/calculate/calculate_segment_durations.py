def calculate_segment_durations(segments, word_timings, include_se=False):
    """
    Calculates the duration for each segment based on a sequential list of word timings.
    
    Args:
        segments (list): List of dictionaries containing content and word lists.
        word_timings (list): Global list of word timing dictionaries.
        include_se: weather to include start and end time for a segment
        
    Returns:
        list: The updated segments list with 'duration' keys added.
    """
    # Create a copy to avoid modifying the original list in place (optional but good practice)
    processed_segments = [seg.copy() for seg in segments]
    
    # This cursor tracks our position in the global word_timings list
    current_timing_index = 0
    total_timings = len(word_timings)

    for segment in processed_segments:
        # Get the list of words in the current segment
        segment_words = segment.get("words", [])
        word_count = len(segment_words)
        
        # If the segment has no words (e.g., a pure pause or empty segment), skip or set duration to 0
        if word_count == 0:
            segment["duration"] = 0.0
            continue

        # Check if we have enough timings left in the global list
        if current_timing_index + word_count > total_timings:
            print(f"Warning: Not enough timings for segment: {segment.get('content')}")
            break

        # Get the start time of the first word in this segment
        start_time = word_timings[current_timing_index]['start']
        
        # Get the end time of the last word in this segment
        # We look ahead by (word_count - 1) indices
        end_time = word_timings[current_timing_index + word_count - 1]['end']
        
        # Calculate duration
        duration = end_time - start_time
        
        # Add to segment (rounded to 3 decimal places for cleanliness)
        segment["duration"] = round(duration, 3)

        if include_se:
          segment["start_time"] = round(start_time, 3)
          segment["end_time"] = round(end_time, 3)
        
        # Move the cursor forward so the next segment starts where this one left off
        current_timing_index += word_count

    return processed_segments

if __name__ == "__main__":
  segments_input = [
    {
      "type": "text",
      "content": "Atomic energy is",
      "words": ["Atomic", "energy", "is"]
    },
    {
      "type": "gif",
      "content": "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif",
      "words": ["the", "energy", "released", "from", "splitting", "atoms."]
    }
  ]

  timings_input = [
  {'word': 'Atomic', 'start': 0.0, 'end': 0.476},
  {'word': 'energy', 'start': 0.546, 'end': 0.882},
  {'word': 'is', 'start': 0.929, 'end': 0.998},
  {'word': 'the', 'start': 1.044, 'end': 1.114},
  {'word': 'energy', 'start': 1.207, 'end': 1.532},
  {'word': 'released', 'start': 1.613, 'end': 1.962},
  {'word': 'from', 'start': 1.996, 'end': 2.136},
  {'word': 'splitting', 'start': 2.217, 'end': 2.6},
  {'word': 'atoms.', 'start': 2.67, 'end': 3.25}
  ]

  result = calculate_segment_durations(segments_input, timings_input,include_se=True)

  import json
  print(json.dumps(result, indent=2))