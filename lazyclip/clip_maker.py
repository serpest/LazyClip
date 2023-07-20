from PIL import Image
from tempfile import TemporaryDirectory
from math import log10
from moviepy.editor import AudioFileClip, ImageSequenceClip

def resize_image_with_padding(image, target_size):
    target_width, target_height = target_size
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    if target_width / target_height > aspect_ratio: # Horizontal padding
        new_width = int(target_height * aspect_ratio)
        new_height = target_height
    else: # Vertical padding
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    resized_image = image.resize((new_width, new_height))
    padded_image = Image.new("RGB", (target_width, target_height))
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2
    padded_image.paste(resized_image, (x_offset, y_offset))
    return padded_image

def generate_image_sequence_clip(audio_path, image_paths, image_durations, frame_size, frame_rate, clip_path):
    clip_duration = sum(image_durations)
    with TemporaryDirectory() as resized_image_dir:
        index = 0
        for image_path in image_paths:
            image = Image.open(image_path)
            resized_image = resize_image_with_padding(image, frame_size)
            resized_image_filename = str(index).zfill(int(log10(len(image_paths)-1))+1) + ".jpg" # Add leading zeros
            resized_image.save(f"{resized_image_dir}/{resized_image_filename}", "JPEG")
            index += 1
        clip = ImageSequenceClip(resized_image_dir, durations=image_durations)
        audio_clip = AudioFileClip(audio_path)
        if (clip_duration < audio_clip.duration):
            audio_clip = audio_clip.set_end(clip_duration)
        clip.audio = audio_clip
        clip.write_videofile(clip_path, fps=frame_rate)
        clip.close()
