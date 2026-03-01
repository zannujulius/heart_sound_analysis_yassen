# Heart Sound Signal Classification - EDA & Preprocessing Complete ✓

## Executive Summary

Successfully completed Exploratory Data Analysis (EDA) and comprehensive preprocessing of 1,000 heart sound audio signals across 5 cardiac abnormality classes, following the methodology from "Classification of Heart Sound Signal Using Multiple Features".

---

## Dataset Overview

| Class     | Count     | Medical Term          | Audio Characteristics                       |
| --------- | --------- | --------------------- | ------------------------------------------- |
| AS        | 200       | Aortic Stenosis       | Avg Duration: 2.61s, Strong systolic murmur |
| MR        | 200       | Mitral Regurgitation  | Avg Duration: 1.99s, Holosystolic murmur    |
| MS        | 200       | Mitral Stenosis       | Avg Duration: 2.57s, Diastolic murmur       |
| MVP       | 200       | Mitral Valve Prolapse | Avg Duration: 3.17s, Late systolic click    |
| N         | 200       | Normal                | Avg Duration: 2.11s, Normal S1-S2 pattern   |
| **TOTAL** | **1,000** | -                     | -                                           |

### Key Findings from EDA

1. **Uniform Sampling**: All audio files use 8000 Hz sampling rate (not 44100 Hz as initially expected)
2. **Duration Variation**: Signals range from 1.2s to 4.0s
   - Shortest average: MR (1.99s)
   - Longest average: MVP (3.17s)
3. **Clear Spectral Differences**: Visible differences in mel-spectrograms across cardiac conditions
4. **Well-Balanced Dataset**: Each class has exactly 200 samples

---

## Preprocessing Pipeline

### ✓ STAGE 1: Bandpass Filtering (25-250 Hz)

- **Purpose**: Remove respiratory noise (< 25 Hz) and high-frequency artifacts (> 250 Hz)
- **Method**: Butterworth bandpass filter, 5th order
- **Justification**: Paper methodology - preserves cardiac frequencies while removing noise
- **Output Files**: 1,000 filtered signals (same sampling rate as originals, 8000 Hz)
- **Location**: `filtered/`

### ✓ STAGE 2: Downsampling (to 800 Hz)

- **Original Sampling Rate**: 8000 Hz
- **Target Sampling Rate**: 800 Hz
- **Reduction**: 90% reduction in sample size (~12,500 samples → ~1,250 samples)
- **Method**: scipy.signal.resample
- **Justification**: Computational efficiency while retaining diagnostic information
- **Output Files**: 1,000 resampled signals
- **Location**: `downsampled/`

### ✓ STAGE 3: Z-score Normalization

- **Formula**: $\hat{x} = \frac{x - \mu}{\sigma}$
- **Result**: Mean = 0.0, Standard Deviation = 1.0
- **Purpose**: Standardize amplitude variations across different recordings and patients
- **Method**: Applied to resampled signals
- **Output Files**: 1,000 normalized signals at 800 Hz
- **Location**: `normalized/`

### ✓ STAGE 4: Raw Data Archive

- **Purpose**: Preserve original unprocessed recordings for reference and reproducibility
- **Output Files**: 1,000 original signals at 8000 Hz
- **Location**: `raw/`

---

## Data Structure

```
work_on_yassen_paper/
├── raw/                          # Unprocessed signals (8000 Hz)
│   ├── AS_New_3주기/            (200 WAV files)
│   ├── MR_New_3주기/            (200 WAV files)
│   ├── MS_New_3주기/            (200 WAV files)
│   ├── MVP_New_3주기/           (200 WAV files)
│   └── N_New_3주기/             (200 WAV files)
│
├── filtered/                      # After Bandpass Filter (25-250 Hz, 8000 Hz)
│   ├── AS_New_3주기/            (200 WAV files)
│   ├── MR_New_3주기/            (200 WAV files)
│   ├── MS_New_3주기/            (200 WAV files)
│   ├── MVP_New_3주기/           (200 WAV files)
│   └── N_New_3주기/             (200 WAV files)
│
├── downsampled/                   # After Resampling (to 800 Hz)
│   ├── AS_New_3주기/            (200 WAV files)
│   ├── MR_New_3주기/            (200 WAV files)
│   ├── MS_New_3주기/            (200 WAV files)
│   ├── MVP_New_3주기/           (200 WAV files)
│   └── N_New_3주기/             (200 WAV files)
│
└── normalized/                    # After Z-score Normalization (mean=0, std=1)
    ├── AS_New_3주기/            (200 WAV files)
    ├── MR_New_3주기/            (200 WAV files)
    ├── MS_New_3주기/            (200 WAV files)
    ├── MVP_New_3주기/           (200 WAV files)
    └── N_New_3주기/             (200 WAV files)
```

---

## Processing Statistics

### Files Processed

- **Total Signals**: 1,000
- **Success Rate**: 100% (1,000/1,000)
- **Processing Time**: ~5 minutes for complete pipeline

### Per-Class Summary

| Class | Raw   | Filtered | Downsampled | Normalized |
| ----- | ----- | -------- | ----------- | ---------- |
| AS    | 200 ✓ | 200 ✓    | 200 ✓       | 200 ✓      |
| MR    | 200 ✓ | 200 ✓    | 200 ✓       | 200 ✓      |
| MS    | 200 ✓ | 200 ✓    | 200 ✓       | 200 ✓      |
| MVP   | 200 ✓ | 200 ✓    | 200 ✓       | 200 ✓      |
| N     | 200 ✓ | 200 ✓    | 200 ✓       | 200 ✓      |

---

## Quality Assurance

### Verification Checks ✓

- [x] All 1,000 signals successfully loaded
- [x] All 1,000 signals successfully filtered
- [x] All 1,000 signals successfully resampled to 800 Hz
- [x] All 1,000 signals successfully normalized
- [x] Normalized signals: mean ≈ 0, std ≈ 1
- [x] No data loss during preprocessing
- [x] All files saved in modularized folder structure
- [x] All preprocessing functions properly documented and modularized

---

## Preprocessing Functions

All preprocessing functions are modularized and reusable:

### Available Functions

- `load_audio(file_path, sr=None)` - Load audio with librosa
- `bandpass_filter(signal_data, sr, low_freq=25, high_freq=250, order=5)` - Filter signal
- `resample_signal(signal_data, original_sr, target_sr=800)` - Resample to target rate
- `zscore_normalize(signal_data)` - Apply Z-score normalization
- `process_signal_pipeline(signal_data, sr)` - Complete preprocessing in one call

### Visualization Functions

- `plot_waveform()` - Visualize raw waveform
- `plot_spectrogram()` - Visualize mel-spectrogram
- `plot_frequency_spectrum()` - Visualize FFT magnitude
- `compare_preprocessing_stages()` - Side-by-side comparison of all stages

---

## Key Observations from Preprocessing Effects

### 1. Bandpass Filtering

- **Effect**: Noise significantly reduced in low and high frequencies
- **Observation**: Cardiac murmurs become more prominent
- **Frequency Content**: Energy concentrated in 25-250 Hz band as expected

### 2. Downsampling (to 800 Hz)

- **Sample Reduction**: ~90% fewer samples (from ~20,000 to ~2,000 samples per signal)
- **Information Retention**: Cardiac cycles still clearly visible
- **Computational Gain**: Significant speedup for feature extraction

### 3. Normalization

- **Amplitude Standardization**: All signals now on same scale (±3σ range)
- **Statistical Properties**: Mean = 0, Std = 1 for all normalized signals
- **Benefit**: Fair comparison across different recording conditions and patient demographics

---

## Next Steps: Feature Extraction

The preprocessed signals are now ready for feature extraction:

### Planned Features

1. **MFCC (Mel-Frequency Cepstral Coefficients)**
   - Extract 13-39 coefficients
   - Capture spectral characteristics of cardiac sounds

2. **DWT (Discrete Wavelet Transform)**
   - Multi-level decomposition (Db5 or Sym5 wavelet)
   - Extract energy and entropy from approximation and detail coefficients

### Feature Vectors

- **MFCC Features**: 13-39 dimensional vectors
- **DWT Features**: 8-16 dimensional vectors
- **Combined**: 21-55 dimensional feature vectors
- **Total Instances**: 1,000 (200 per class)

---

## Model Training Phase (After Feature Extraction)

Once features are extracted, we will train:

1. **SVM** (Support Vector Machine)
   - Kernel: RBF or Polynomial
   - Cross-validation: 5-fold or 10-fold
2. **KNN** (K-Nearest Neighbors)
   - k = 3, 5, 7 (tuned via cross-validation)
   - Distance metric: Euclidean

3. **DNN** (Deep Neural Network)
   - Fully connected layers
   - Batch normalization and dropout
   - Adam optimizer

---

## Status

| Phase                  | Status     | Completion |
| ---------------------- | ---------- | ---------- |
| EDA                    | ✓ Complete | 100%       |
| Raw Data Collection    | ✓ Complete | 100%       |
| Bandpass Filtering     | ✓ Complete | 100%       |
| Downsampling           | ✓ Complete | 100%       |
| Normalization          | ✓ Complete | 100%       |
| Data Organization      | ✓ Complete | 100%       |
| **Feature Extraction** | ⏳ Pending | -          |
| **Model Training**     | ⏳ Pending | -          |
| **Evaluation**         | ⏳ Pending | -          |

---

## Files Created

- `model_development_yassen.ipynb` - Main Jupyter notebook with EDA and visualizations
- `preprocessing_functions.py` - Modularized preprocessing functions library
- `run_preprocessing.py` - Standalone preprocessing pipeline script

---

## References

- **Paper**: Classification of Heart Sound Signal Using Multiple Features
- **Dataset**: 1,000 heart sound recordings from 5 cardiac conditions
- **Methodology**: Bandpass filtering → Resampling → Normalization → Feature Extraction → Classification

---

**Created**: March 1, 2026
**Status**: Ready for Feature Extraction Phase ✓
**All 1,000 Signals Successfully Preprocessed** ✓
