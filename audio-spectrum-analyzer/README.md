# Audio Spectrum Analyzer

This project is an audio spectrum analyzer application built in Python. It allows users to upload audio files and visualize their frequency spectrum using Fourier Transform techniques. The application also includes functionality to filter specific frequency ranges.

## Project Structure

```
audio-spectrum-analyzer
├── src
│   ├── main.py               # Entry point of the application
│   ├── audio_processor.py     # Handles audio processing and Fourier Transform
│   ├── gui
│   │   ├── __init__.py       # Initializes the GUI package
│   │   └── window.py          # Main application window and interface
│   └── utils
│       ├── __init__.py       # Initializes the utilities package
│       └── filters.py         # Frequency filtering functions
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd audio-spectrum-analyzer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/main.py
   ```
2. Use the interface to upload an audio file and visualize its frequency spectrum.
3. Utilize the filtering options to isolate specific frequency ranges.

## Dependencies

- numpy
- scipy
- matplotlib

## License

This project is licensed under the MIT License.