import librosa
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

audio_path = "audios/0.wav"
sampling_rate = 10 # In hertz
interval = 3 # In seconds

samples, sampling_rate = librosa.load(audio_path, sr=sampling_rate, mono=True)

samples = librosa.amplitude_to_db(samples)
peaks_indexes, _ = find_peaks(samples, distance=interval*sampling_rate, prominence=1)

plt.plot(samples)
plt.plot(peaks_indexes, samples[peaks_indexes], "xr")
plt.show()
