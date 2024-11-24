from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from audio_processor import AudioProcessor
from utils.filters import high_pass_filter
import numpy as np
import librosa.display

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Spectrum Analyzer")
        self.audio_processor = AudioProcessor()
        self.setup_ui()

    def setup_ui(self):
        # Crear widget central y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Botón para subir audio
        self.upload_button = QPushButton("Upload Audio")
        self.upload_button.clicked.connect(self.on_upload)
        layout.addWidget(self.upload_button)

        # Botón para filtrar bajos
        self.filter_button = QPushButton("Filter Bass")
        self.filter_button.clicked.connect(self.filter_frequency)
        layout.addWidget(self.filter_button)

        # Canvas para gráficos
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def on_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav)")
        if file_path:
            self.audio_processor.load_audio(file_path)
            self.plot_spectrum()

    def plot_spectrum(self):
        self.figure.clear()
        grid = self.figure.add_gridspec(2, 1, height_ratios=[1, 1.5])
        ax_spectrum = self.figure.add_subplot(grid[0])
        ax_spectrogram = self.figure.add_subplot(grid[1])

        # Calcular y mostrar el espectro de frecuencias (Transformada de Fourier)
        freqs, magnitude_db = self.audio_processor.get_frequency_spectrum()
        ax_spectrum.plot(freqs, magnitude_db, label='Original', alpha=0.7, color='blue')
        ax_spectrum.set_xlabel('Frecuencia (Hz)')
        ax_spectrum.set_ylabel('Magnitud (dB)')
        ax_spectrum.set_title('Espectro de Frecuencias')
        ax_spectrum.grid(True)
        ax_spectrum.set_xlim(0, 2000)  # Mostrar frecuencias hasta 2000 Hz

        # Calcular y mostrar el espectrograma
        _, stft_db = self.audio_processor.get_spectrogram()
        librosa.display.specshow(stft_db, sr=self.audio_processor.sample_rate, hop_length=512, x_axis='time', y_axis='linear', cmap='viridis', ax=ax_spectrogram)
        ax_spectrogram.set_ylabel('Frecuencia (Hz)')
        ax_spectrogram.set_xlabel('Tiempo (s)')
        ax_spectrogram.set_title('Espectrograma')
        ax_spectrogram.set_ylim(0, 2000)  # Limitar frecuencias hasta 2000 Hz

        self.figure.tight_layout()
        self.canvas.draw()

    def filter_frequency(self):
        if self.audio_processor.audio_data is not None:
            # Guardar datos originales antes del filtrado
            original_data = self.audio_processor.audio_data.copy()
            
            # Aplicar filtro paso alto para remover bajos (frecuencias < 200Hz)
            filtered_data = high_pass_filter(self.audio_processor.audio_data, 
                                             cutoff=200,  
                                             fs=self.audio_processor.sample_rate)
            
            self.audio_processor.audio_data = filtered_data
            
            # Mostrar ambos espectros
            self.figure.clear()
            grid = self.figure.add_gridspec(2, 1, height_ratios=[1, 1.5])
            ax_spectrum = self.figure.add_subplot(grid[0])
            ax_spectrogram = self.figure.add_subplot(grid[1])
            
            # Obtener y graficar espectro original
            self.audio_processor.audio_data = original_data
            freqs, spectrum_orig = self.audio_processor.get_frequency_spectrum()
            
            # Obtener y graficar espectro filtrado
            self.audio_processor.audio_data = filtered_data
            _, spectrum_filt = self.audio_processor.get_frequency_spectrum()
            
            # Solo mostrar frecuencias positivas hasta 2000Hz
            mask = (freqs >= 0) & (freqs <= 2000)
            freqs = freqs[mask]
            spectrum_orig = spectrum_orig[mask]
            spectrum_filt = spectrum_filt[mask]
            
            ax_spectrum.plot(freqs, spectrum_orig, label='Original', alpha=0.7)
            ax_spectrum.plot(freqs, spectrum_filt, label='Filtered', alpha=0.7)
            ax_spectrum.axvspan(0, 200, color='red', alpha=0.2, label='Bass Region')
            ax_spectrum.set_xlabel('Frecuencia (Hz)')
            ax_spectrum.set_ylabel('Magnitud (dB)')
            ax_spectrum.set_title('Espectro de Frecuencias')
            ax_spectrum.grid(True)
            ax_spectrum.legend()
            ax_spectrum.set_xlim(0, 2000)  # Mostrar frecuencias hasta 2000 Hz
            
            # Calcular y mostrar el espectrograma del audio filtrado
            _, stft_db = self.audio_processor.get_spectrogram()
            librosa.display.specshow(stft_db, sr=self.audio_processor.sample_rate, hop_length=512, x_axis='time', y_axis='linear', cmap='viridis', ax=ax_spectrogram)
            ax_spectrogram.set_ylabel('Frecuencia (Hz)')
            ax_spectrogram.set_xlabel('Tiempo (s)')
            ax_spectrogram.set_title('Espectrograma')
            ax_spectrogram.set_ylim(0, 2000)  # Limitar frecuencias hasta 2000 Hz

            self.figure.tight_layout()
            self.canvas.draw()