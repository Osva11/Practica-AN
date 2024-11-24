import numpy as np
from scipy.io import wavfile
import librosa

class AudioProcessor:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.MAX_DURATION = 30

    def load_audio(self, file_path):
        try:
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            # Convertir a mono si es estéreo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            # Limitar duración
            max_samples = int(self.MAX_DURATION * sample_rate)
            if len(audio_data) > max_samples:
                audio_data = audio_data[:max_samples]
            self.sample_rate = sample_rate
            self.audio_data = audio_data
        except FileNotFoundError:
            print(f"Error: El archivo {file_path} no se encuentra.")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def get_frequency_spectrum(self):
        if self.audio_data is None:
            raise ValueError("No audio loaded")
        
        # Aplicar ventana de Hanning
        window = np.hanning(len(self.audio_data))
        audio_windowed = self.audio_data * window
        
        # Calcular la FFT
        n = len(audio_windowed)
        fft_data = np.fft.fft(audio_windowed)
        freqs = np.fft.fftfreq(n, d=1/self.sample_rate)
        
        # Obtener solo la mitad positiva del espectro
        pos_mask = freqs >= 0
        freqs = freqs[pos_mask]
        magnitude = np.abs(fft_data[pos_mask])
        
        # Convertir la magnitud a escala dB
        magnitude_db = 20 * np.log10(magnitude + 1e-10)
        
        return freqs, magnitude_db

    def get_spectrogram(self, n_fft=2048, hop_length=512):
        if self.audio_data is None:
            raise ValueError("No audio loaded")
        
        # Calcular STFT
        stft_result = librosa.stft(self.audio_data, n_fft=n_fft, hop_length=hop_length)
        stft_db = librosa.amplitude_to_db(np.abs(stft_result), ref=np.max)
        
        return stft_result, stft_db