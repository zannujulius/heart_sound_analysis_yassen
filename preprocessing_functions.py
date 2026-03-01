"""
Heart Sound Signal Preprocessing Functions
============================================

Modularized preprocessing functions for heart sound classification.
Implements the methodology from "Classification of Heart Sound Signal Using Multiple Features"

Functions:
- load_audio: Load audio files using librosa
- bandpass_filter: Apply Butterworth bandpass filter (25-250 Hz)
- resample_signal: Downsample to 800 Hz
- zscore_normalize: Z-score normalization
- process_signal_pipeline: Complete preprocessing pipeline
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from pathlib import Path


# Preprocessing parameters
BANDPASS_LOW = 25      # Low frequency cutoff (Hz)
BANDPASS_HIGH = 250    # High frequency cutoff (Hz)
TARGET_SR = 800        # Target sampling rate (Hz)


def load_audio(file_path, sr=None):
    """
    Load audio file using librosa.
    
    Parameters
    ----------
    file_path : str or Path
        Path to audio file
    sr : int, optional
        Target sampling rate. If None, uses native sample rate
        
    Returns
    -------
    y : np.ndarray
        Audio time series
    sr : int
        Sampling rate
    """
    y, sr = librosa.load(str(file_path), sr=sr, mono=True)
    return y, sr


def bandpass_filter(signal_data, sr, low_freq=BANDPASS_LOW, high_freq=BANDPASS_HIGH, order=5):
    """
    Apply Butterworth bandpass filter to audio signal.
    
    This filter removes low-frequency noise (e.g., respiration) and high-frequency
    noise while preserving the heart sound frequencies as per the paper methodology.
    
    Parameters
    ----------
    signal_data : np.ndarray
        Input audio signal
    sr : int
        Sampling rate
    low_freq : float
        Low cutoff frequency (Hz)
    high_freq : float
        High cutoff frequency (Hz)
    order : int
        Filter order (higher = steeper)
        
    Returns
    -------
    np.ndarray
        Filtered audio signal
    """
    # Normalize frequencies to Nyquist frequency
    nyquist = sr / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    
    # Ensure frequencies are valid
    low = np.clip(low, 0.001, 0.999)
    high = np.clip(high, low + 0.001, 0.999)
    
    # Design Butterworth bandpass filter
    b, a = signal.butter(order, [low, high], btype='band')
    
    # Apply filter
    filtered = signal.filtfilt(b, a, signal_data)
    
    return filtered


def resample_signal(signal_data, original_sr, target_sr=TARGET_SR):
    """
    Resample audio signal to target sampling rate.
    
    Downsamples to 800 Hz for computational efficiency while retaining
    important cardiac information per the paper methodology.
    
    Parameters
    ----------
    signal_data : np.ndarray
        Input audio signal
    original_sr : int
        Original sampling rate
    target_sr : int
        Target sampling rate
        
    Returns
    -------
    np.ndarray
        Resampled signal at target_sr
    """
    if original_sr == target_sr:
        return signal_data
    
    # Calculate number of samples in resampled signal
    num_samples = int(len(signal_data) * target_sr / original_sr)
    
    # Use librosa's high-quality resampling
    resampled = librosa.resample(signal_data, orig_sr=original_sr, target_sr=target_sr, res_type='kaiser_best')
    
    return resampled


def zscore_normalize(signal_data):
    """
    Apply Z-score normalization to audio signal.
    
    Normalizes signal to mean=0 and std=1 to handle amplitude variations
    across different recordings as per the paper methodology.
    
    Parameters
    ----------
    signal_data : np.ndarray
        Input audio signal
        
    Returns
    -------
    np.ndarray
        Normalized signal
    """
    mean = np.mean(signal_data)
    std = np.std(signal_data)
    
    # Avoid division by zero
    if std == 0:
        return signal_data - mean
    
    normalized = (signal_data - mean) / std
    
    return normalized


def process_signal_pipeline(signal_data, sr, verbose=False):
    """
    Apply complete preprocessing pipeline: filter -> resample -> normalize.
    
    Parameters
    ----------
    signal_data : np.ndarray
        Input raw audio signal
    sr : int
        Original sampling rate
    verbose : bool
        Print processing steps
        
    Returns
    -------
    tuple
        (filtered_signal, resampled_signal, normalized_signal, new_sr)
    """
    if verbose:
        print(f"  Original signal: {len(signal_data)} samples @ {sr} Hz")
    
    # Step 1: Bandpass filter
    filtered = bandpass_filter(signal_data, sr)
    if verbose:
        print(f"  After filter: {len(filtered)} samples (freq: {BANDPASS_LOW}-{BANDPASS_HIGH} Hz)")
    
    # Step 2: Resample
    resampled = resample_signal(filtered, sr, TARGET_SR)
    if verbose:
        print(f"  After resample: {len(resampled)} samples @ {TARGET_SR} Hz")
    
    # Step 3: Normalize
    normalized = zscore_normalize(resampled)
    if verbose:
        print(f"  After normalization: mean={np.mean(normalized):.2e}, std={np.std(normalized):.2f}")
    
    return filtered, resampled, normalized, TARGET_SR
