import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from lazyclip.audio_analyzer import fragment_audio
from lazyclip.clip_maker import generate_image_sequence_clip

class LazyClip(toga.App):
    def startup(self):
        # Audio path box
        audio_path_label = toga.Label(
            "Audio path: ",
            style=Pack(padding=(0, 5))
        )
        self.audio_path_input = toga.TextInput(style=Pack(flex=1))
        audio_path_selection_button = toga.Button("...", on_press=self.select_audio_path_from_files, style=Pack(padding_right=5, padding_left=5))
        audio_path_box = toga.Box(style=Pack(direction=ROW, padding=5))
        audio_path_box.add(audio_path_label)
        audio_path_box.add(self.audio_path_input)
        audio_path_box.add(audio_path_selection_button)
        # Image paths box
        image_paths_label = toga.Label(
            "Image paths: ",
            style=Pack(padding=(0, 5))
        )
        self.image_paths_input = toga.TextInput(style=Pack(flex=1))
        image_paths_selection_button = toga.Button("...", on_press=self.select_image_paths_from_files, style=Pack(padding_right=5, padding_left=5))
        image_paths_box = toga.Box(style=Pack(direction=ROW, padding=5))
        image_paths_box.add(image_paths_label)
        image_paths_box.add(self.image_paths_input)
        image_paths_box.add(image_paths_selection_button)
        # Clip path box
        clip_path_label = toga.Label(
            "Clip path: ",
            style=Pack(padding=(0, 5))
        )
        self.clip_path_input = toga.TextInput(style=Pack(flex=1))
        clip_path_selection_button = toga.Button("...", on_press=self.select_clip_path_for_saving, style=Pack(padding_right=5, padding_left=5))
        clip_path_box = toga.Box(style=Pack(direction=ROW, padding=5))
        clip_path_box.add(clip_path_label)
        clip_path_box.add(self.clip_path_input)
        clip_path_box.add(clip_path_selection_button)
        # Generation button
        generation_button = toga.Button("Generate clip", on_press=self.generate_clip, style=Pack(padding_right=5, padding_left=5, padding_top = 10))
        # Main box
        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(audio_path_box)
        main_box.add(image_paths_box)
        main_box.add(clip_path_box)
        main_box.add(generation_button)
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

    def select_image_paths_from_files(self, widget):
        self.main_window.open_file_dialog(title="Images selection", multiselect=True, on_result=self.update_image_paths_input)

    def update_image_paths_input(self, widget, paths):
        if paths is None:
            return
        number_of_paths = len(paths)
        if number_of_paths == 1:
            self.image_paths_input.value = paths[0]
        else:
            new_value = ""
            for i in range(number_of_paths):
                new_value += f"\"{paths[i]}\""
                if i < number_of_paths - 1:
                    new_value += ", "
            self.image_paths_input.value = new_value

    def select_clip_path_for_saving(self, widjet):
        self.main_window.save_file_dialog("Clip path selection", "clip.mp4", on_result=self.update_clip_path_input)

    def update_clip_path_input(self, widget, path):
        if path is None:
            return
        self.clip_path_input.value = str(path)

    def generate_clip(self, widget):
        # TODO
        audio_path = self.audio_path_input.value
        number_of_images = 0 # TODO
        image_paths = [] # TODO
        clip_path = self.clip_path_input.value
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
        self.main_window.info_dialog("Clip generated", f"Clip correctly saved as {clip_path}")

def main():
    return LazyClip()
