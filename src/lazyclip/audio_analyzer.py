import librosa
import numpy
from scipy.signal import find_peaks

def fragment_audio(audio_path, min_duration, max_duration, sampling_rate=10):
    amplitude_samples, sampling_rate = librosa.load(audio_path, sr=sampling_rate, mono=True)
    peaks_indexes = find_audio_peaks(amplitude_samples, sampling_rate, min_duration)
    samples_indexes = adjust_samples_indexes(peaks_indexes, sampling_rate, min_duration, max_duration)
    interval_durations = compute_interval_durations(samples_indexes, sampling_rate)
    return interval_durations

def find_audio_peaks(samples, sampling_rate, peaks_min_distance):
    peaks_min_samples_distance = sampling_rate * peaks_min_distance
    peaks_indexes, _ = find_peaks(samples, distance=peaks_min_samples_distance)
    return peaks_indexes

def adjust_samples_indexes(peaks_indexes, sampling_rate, min_duration, max_duration):
    min_samples_distance = sampling_rate * min_duration
    max_samples_distance = sampling_rate * max_duration
    samples_indexes = peaks_indexes
    # Set the first element of samples_indexes to zero
    if samples_indexes[0] < min_samples_distance:
        samples_indexes[0] = 0
    else:
        samples_indexes = numpy.insert(samples_indexes, 0, 0)
    # Fragment intervals without peaks that are too long
    # TODO: min_duration and max_duration have a certain tolerance with this implementation
    i = 0
    while i < len(samples_indexes) - 1:
        cur_separators_distance = samples_indexes[i + 1] - samples_indexes[i]
        min_number_of_missing_gaps = cur_separators_distance / max_samples_distance # Ceiling omitted
        max_number_of_missing_gaps = cur_separators_distance / min_samples_distance # Flooring omitted
        best_number_of_missing_gaps = round((min_number_of_missing_gaps + max_number_of_missing_gaps) / 2)
        best_number_of_missing_separators = best_number_of_missing_gaps - 1
        for j in range(best_number_of_missing_separators):
            new_separator = samples_indexes[i] + int((j + 1) * (cur_separators_distance / best_number_of_missing_gaps))
            samples_indexes = numpy.insert(samples_indexes, i + j + 1, new_separator)
        i += best_number_of_missing_separators + 1
    return samples_indexes

def compute_interval_durations(samples_indexes, sampling_rate):
    samples_diffs = samples_indexes
    for i in range(len(samples_diffs) - 1, 0, -1):
        samples_diffs[i] -= samples_diffs[i - 1]
    samples_diffs = samples_diffs[1:]
    interval_durations = samples_diffs / sampling_rate
    return interval_durations
