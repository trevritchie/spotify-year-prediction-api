# Model Files

## Pre-trained Model

The trained Random Forest model is provided as a compressed archive due to GitHub's file size limits.

**File:** `model.zip` (31 MB compressed)

## Extraction Instructions

1. Unzip `models/model.zip`
2. Extract the following files to the `models/` directory:
   - `music_year_model.pkl` (144 MB)
   - `feature_names.pkl` (155 bytes)

### Verification

After extraction, you should have:
```
models/
├── model.zip
├── music_year_model.pkl  (extracted)
├── feature_names.pkl     (extracted)
└── README.md
```

The API will automatically load these files when started.

## Model Details

- **Type:** Random Forest Regressor
- **Size:** 144 MB (uncompressed)
- **Training:** 136,522 songs from Spotify (1921-2020)
- **Performance:** R² = 0.6804, MAE = 10.72 years

