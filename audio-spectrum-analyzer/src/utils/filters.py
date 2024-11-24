def low_pass_filter(data, cutoff, fs):
    from scipy.signal import butter, lfilter

    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(1, normal_cutoff, btype='low', analog=False)
    filtered_data = lfilter(b, a, data)
    return filtered_data


def high_pass_filter(data, cutoff, fs, order=4):
    from scipy.signal import butter, filtfilt

    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data


def band_reject_filter(data, low_cut, high_cut, fs):
    """
    Implementa un filtro de rechazo de banda para eliminar frecuencias entre low_cut y high_cut
    """
    from scipy.signal import butter, sosfilt
    
    nyquist = 0.5 * fs
    low = low_cut / nyquist
    high = high_cut / nyquist
    
    # Crear filtro de rechazo de banda
    sos = butter(4, [low, high], btype='bandstop', output='sos')
    
    # Aplicar filtro
    filtered_data = sosfilt(sos, data)
    
    return filtered_data