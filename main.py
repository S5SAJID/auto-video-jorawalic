import questionary
from halo import Halo
from utils.generate_audio_video import generate_audio_video
from lib.ai.ideas_generator import generate_ideas

def main():
    general_field = questionary.text("General field:").ask()

    if not general_field:
        return

    # Keep the spinner OUTSIDE the Mute context so we can see it
    spinner = Halo(text='Initializing...', spinner='dots', color='cyan')
    spinner.start()

    spinner.text = "Generating ideas"

    video_ideas = generate_ideas(general_topic=general_field)

    spinner.text = "Starting engine"

    videos_selected = questionary.checkbox("Which videos to generate?", choices=[idea['title'] for idea in video_ideas]).ask() 

    videos_selected = [idea for idea in video_ideas if idea['title'] in videos_selected]
    
    try:
        for selected_video in videos_selected:
            spinner.text = f"Generating video: \"{selected_video['title']}\""
            for status in generate_audio_video(title=f"Generate video with title: \"{selected_video['title']}\" with the script outline something like \"{selected_video['script_outline']}\""):
                spinner.text = status
         
    except Exception as e:
        spinner.fail(f"Error: {e}")
    finally:
        spinner.succeed("Video processing complete!")

if __name__ == "__main__":
    main()