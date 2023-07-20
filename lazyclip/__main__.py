from lazyclip.audio_analyzer import fragment_audio
from lazyclip.clip_maker import generate_image_sequence_clip

audio_path = input("Enter the audio path: ")
number_of_images = int(input("Enter the number of images: "))
image_paths = []
for i in range(number_of_images):
    new_image_path = input(f"Enter image {i + 1} path: ")
    image_paths.append(new_image_path)
clip_path = input("Enter clip path: ")

frame_size = (1920, 1080)
frame_rate = 30
min_image_duration = 2 # In seconds
max_image_duration = 6 # In seconds

print("Fragmenting audio...")
audio_interval_durations = fragment_audio(audio_path, min_image_duration, max_image_duration)
image_durations = audio_interval_durations[:number_of_images]
print("Audio fragmented.")

print("Generating clip...")
generate_image_sequence_clip(audio_path, image_paths, image_durations, clip_path, frame_size, frame_rate)
print("Clip generated.")
