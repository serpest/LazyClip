import librosa
from scipy.signal import find_peaks
import pygame
import time

filename = "audios/0.wav"
sampling_rate = 10 # In hertz
interval = 1.5 # In seconds

samples, sampling_rate = librosa.load(filename, sr=sampling_rate, mono=True)

samples = librosa.amplitude_to_db(samples)
peaks_indexes, _ = find_peaks(samples, distance=interval*sampling_rate, prominence=1)

peaks_indexes_set = set(peaks_indexes)
pygame.mixer.init()
sound = pygame.mixer.Sound(filename)
pygame.display.set_caption("Audio peaks flashing viewer")
display = pygame.display.set_mode((500, 500))
start_time = time.time() * 1000 # In milliseconds
end_time = start_time + int(sound.get_length() * 1000) # In milliseconds
end_flag = False
sound.play()
while not end_flag:
    # Assuming that every iteration is fast enough
    cur_time = time.time() * 1000 # In milliseconds
    if (cur_time > end_time):
        end_flag = True
    else:
        if int((cur_time - start_time) / 1000 * sampling_rate + 1) in peaks_indexes_set:
            display.fill(pygame.Color(255, 0, 0))
            pygame.display.flip()
            pygame.time.wait(int(1000 / sampling_rate * 3))
        else:
            display.fill(pygame.Color(0, 0, 0))
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_flag = True
pygame.quit()
