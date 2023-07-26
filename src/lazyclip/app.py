import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from concurrent.futures import ThreadPoolExecutor

from lazyclip.audio_analyzer import fragment_audio
from lazyclip.clip_maker import generate_image_sequence_clip

class LazyClip(toga.App):
    def startup(self):
        # Audio path box
        audio_path_label = toga.Label("Audio path:", style=Pack(padding=(0, 5)))
        self.audio_path_input = toga.TextInput(style=Pack(flex=1))
        audio_path_select_button = toga.Button("...", on_press=self.select_audio_path_from_files, style=Pack(padding_right=5, padding_left=5))
        audio_path_box = toga.Box(style=Pack(direction=ROW, padding_right=5, padding_left=5, padding_top = 10))
        audio_path_box.add(audio_path_label)
        audio_path_box.add(self.audio_path_input)
        audio_path_box.add(audio_path_select_button)
        # Image paths box
        self.image_paths_input = toga.MultilineTextInput()
        image_paths_add_button = toga.Button("Add image paths", on_press=self.add_image_paths_from_files)
        image_paths_box = toga.Box(style=Pack(direction=COLUMN, padding_right=5, padding_left=5, padding_top = 10))
        image_paths_box.add(self.image_paths_input)
        image_paths_box.add(image_paths_add_button)
        # Clip path box
        clip_path_label = toga.Label("Clip path:", style=Pack(padding=(0, 5)))
        self.clip_path_input = toga.TextInput(style=Pack(flex=1))
        clip_path_select_button = toga.Button("...", on_press=self.select_clip_path_for_saving, style=Pack(padding_right=5, padding_left=5))
        clip_path_box = toga.Box(style=Pack(direction=ROW, padding_right=5, padding_left=5, padding_top = 10))
        clip_path_box.add(clip_path_label)
        clip_path_box.add(self.clip_path_input)
        clip_path_box.add(clip_path_select_button)
        # Generation button
        self.generation_button = toga.Button("Generate clip", on_press=self.handle_clip_generation, style=Pack(padding_right=5, padding_left=5, padding_top = 10))
        # Main box
        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(audio_path_box)
        main_box.add(image_paths_box)
        main_box.add(clip_path_box)
        main_box.add(self.generation_button)
        # Main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def select_audio_path_from_files(self, widget):
        self.main_window.open_file_dialog(title="Audio selection", multiselect=False, on_result=self.update_audio_path_input)

    def update_audio_path_input(self, widget, path):
        if path is None:
            return
        self.audio_path_input.value = str(path)

    def add_image_paths_from_files(self, widget):
        self.main_window.open_file_dialog(title="Images selection", multiselect=True, on_result=self.add_image_paths_to_list)

    def add_image_paths_to_list(self, widget, paths):
        if paths is None:
            return
        for path in paths:
            self.image_paths_input.value += str(path) + "\n"

    def select_clip_path_for_saving(self, widjet):
        self.main_window.save_file_dialog("Clip path selection", "clip.mp4", on_result=self.update_clip_path_input)

    def update_clip_path_input(self, widget, path):
        if path is None:
            return
        self.clip_path_input.value = str(path)

    async def handle_clip_generation(self, widjet):
        self.generation_button.enabled = False
        self.generation_button.text = "Generating clip..."
        audio_path = self.audio_path_input.value
        image_paths = self.get_image_paths()
        number_of_images = len(image_paths)
        clip_path = self.clip_path_input.value
        frame_size = (1920, 1080)
        frame_rate = 30
        min_image_duration = 2 # In seconds
        max_image_duration = 6 # In seconds
        with ThreadPoolExecutor(1) as executor:
            future = executor.submit(self.generate_clip, audio_path, number_of_images, image_paths, clip_path, frame_size, frame_rate, min_image_duration, max_image_duration)
            while future.done() is False:
                await asyncio.sleep(1)
            exit_code = future.result()
        self.finalize_clip_generation(exit_code, clip_path)

    def generate_clip(self, audio_path, number_of_images, image_paths, clip_path, frame_size, frame_rate, min_image_duration, max_image_duration):
        try:
            audio_interval_durations = fragment_audio(audio_path, min_image_duration, max_image_duration)
            image_durations = audio_interval_durations[:number_of_images]
            generate_image_sequence_clip(audio_path, image_paths, image_durations, clip_path, frame_size, frame_rate)
            return 0
        except:
            return 1
    
    def finalize_clip_generation(self, exit_code, clip_path):
        if exit_code == 0:
            self.main_window.info_dialog("Clip generated", f"Clip correctly saved as \"{clip_path}\".")
        else:
            self.main_window.error_dialog("Clip not generated", f"The clip could not be generated. Check the correctness of the inputs.")
        self.generation_button.text = "Generate clip"
        self.generation_button.enabled = True

    def get_image_paths(self):
        return [raw_path.strip() for raw_path in self.image_paths_input.value.split("\n") if raw_path != ""]
    
def main():
    return LazyClip()
