#!/usr/bin/env python3
"""
Complete preprocessing pipeline for heart sound signals.
Processes 1000 audio files through bandpass filter, resampling, and normalization.
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from pathlib import Path

BASE_PATH = Path('/Users/zannujulius/Desktop/cmu/Research-CVD/Dec-May-2026/code/work_on_yassen_paper')
CLASSES = ['AS_New_3주기', 'MR_New_3주기', 'MS_New_3주기', 'MVP_New_3주기', 'N_New_3주기']
BANDPASS_LOW = 25
BANDPASS_HIGH = 250
TARGET_SR = 800
PROCESSING_STAGES = {
    'raw': 'raw',
    'downsampled': 'downsampled',
    'filtered': 'filtered',
    'normalized': 'normalized'
}

def load_audio(file_path, sr=None):
    y, sr = librosa.load(str(file_path), sr=sr, mono=True)
    return y, sr

def bandpass_filter(signal_data, sr, low_freq=BANDPASS_LOW, high_freq=BANDPASS_HIGH, order=5):
    nyquist = sr / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    low = np.clip(low, 0.001, 0.999)
    high = np.clip(high, low + 0.001, 0.999)
    b, a = signal.butter(order, [low, high], btype='band')
    filtered = signal.filtfilt(b, a, signal_data)
    return filtered

def resample_signal(signal_data, original_sr, target_sr=TARGET_SR):
    if original_sr == target_sr:
        return signal_data
    # Calculate number of samples in resampled signal
    num_samples = int(len(signal_data) * target_sr / original_sr)
    # Use scipy's resample
    from scipy.signal import resample as scipy_resample
    resampled = scipy_resample(signal_data, num_samples)
    return resampled

def zscore_normalize(signal_data):
    mean = np.mean(signal_data)
    std = np.std(signal_data)
    if std == 0:
        return signal_data - mean
    normalized = (signal_data - mean) / std
    return normalized

def process_signal_pipeline(signal_data, sr):
    filtered = bandpass_filter(signal_data, sr)
    resampled = resample_signal(filtered, sr, TARGET_SR)
    normalized = zscore_normalize(resampled)
    return filtered, resampled, normalized, TARGET_SR

print("\n" + "="*80)
print("EXECUTING PREPROCESSING PIPELINE")
print("="*80)

processing_summary = {}

for class_idx, class_folder in enumerate(CLASSES, 1):
    print(f"\n[{class_idx}/{len(CLASSES)}] Processing {class_folder}...")
    
    audio_files = sorted([f for f in (BASE_PATH / class_folder).glob('*.wav')])
    print(f"  Processing {len(audio_files)} audio files...")
    
    processed_count = 0
    errors = 0
    
    for file_idx, audio_file in enumerate(audio_files, 1):
        try:
            y_raw, sr_original = load_audio(audio_file)
            y_filtered, y_resampled, y_normalized, sr_new = process_signal_pipeline(y_raw, sr_original)
            
            raw_dst = BASE_PATH / PROCESSING_STAGES['raw'] / class_folder / audio_file.name
            sf.write(str(raw_dst), y_raw, sr_original)
            
            downsampled_dst = BASE_PATH / PROCESSING_STAGES['downsampled'] / class_folder / audio_file.name
            sf.write(str(downsampled_dst), y_resampled, sr_new)
            
            filtered_dst = BASE_PATH / PROCESSING_STAGES['filtered'] / class_folder / audio_file.name
            sf.write(str(filtered_dst), y_filtered, sr_original)
            
            normalized_dst = BASE_PATH / PROCESSING_STAGES['normalized'] / class_folder / audio_file.name
            sf.write(str(normalized_dst), y_normalized, sr_new)
            
            processed_count += 1
            
            if (file_idx % 50 == 0) or (file_idx == len(audio_files)):
                print(f"    Progress: {file_idx}/{len(audio_files)} files")
                
        except Exception as e:
            errors += 1
            print(f"    Error: {str(e)}")
    
    processing_summary[class_folder] = {
        'total': len(audio_files),
        'processed': processed_count,
        'errors': errors
    }
    
    print(f"  ✓ Completed: {processed_count}/{len(audio_files)}")

print("\n" + "="*80)
print("PREPROCESSING COMPLETE")
print("="*80)

for class_folder in CLASSES:
    summary = processing_summary[class_folder]
    print(f"{class_folder}: {summary['processed']}/{summary['total']}")

print("\nVerifying output files...")
for stage_name in PROCESSING_STAGES.values():
    total_files = 0
    stage_path = BASE_PATH / stage_name
    for class_folder in CLASSES:
        class_path = stage_path / class_folder
        files = list(class_path.glob('*.wav'))
        total_files += len(files)
    print(f"  {stage_name}: {total_files} total files")

print("\n" + "="*80)
print("✓ PREPROCESSING PIPELINE EXECUTION COMPLETE")
print("="*80)
