"""
FastAPI application for music release year prediction.
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Music Release Year Prediction API",
    description="Predicts the release year of songs (1921-2020) based on Spotify audio features",
    version="1.0.0"
)

# Load model and feature names at startup
MODEL_PATH = Path("models/music_year_model.pkl")
FEATURES_PATH = Path("models/feature_names.pkl")

try:
    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    print(f"[OK] Model loaded successfully from {MODEL_PATH}")
    print(f"[OK] Feature names: {feature_names}")
except FileNotFoundError as e:
    print(f"ERROR: Model file not found - {e}")
    model = None
    feature_names = None
except Exception as e:
    print(f"ERROR: Failed to load model - {e}")
    model = None
    feature_names = None


class SongFeatures(BaseModel):
    """Input model for song audio features"""
    acousticness: float = Field(..., ge=0, le=1, description="Acousticness (0-1)")
    danceability: float = Field(..., ge=0, le=1, description="Danceability (0-1)")
    energy: float = Field(..., ge=0, le=1, description="Energy (0-1)")
    instrumentalness: float = Field(..., ge=0, le=1, description="Instrumentalness (0-1)")
    liveness: float = Field(..., ge=0, le=1, description="Liveness (0-1)")
    loudness: float = Field(..., description="Loudness in dB (typically -60 to 0)")
    speechiness: float = Field(..., ge=0, le=1, description="Speechiness (0-1)")
    tempo: float = Field(..., gt=0, description="Tempo in BPM (typically 50-250)")
    valence: float = Field(..., ge=0, le=1, description="Valence/positivity (0-1)")
    duration_ms: float = Field(..., gt=0, description="Duration in milliseconds")
    key: float = Field(..., ge=0, le=11, description="Musical key (0-11)")
    mode: float = Field(..., ge=0, le=1, description="Mode: 0=minor, 1=major")

    class Config:
        schema_extra = {
            "example": {
                "acousticness": 0.0936,
                "danceability": 0.743,
                "energy": 0.47,
                "instrumentalness": 0.0000315,
                "liveness": 0.186,
                "loudness": -13.154,
                "speechiness": 0.029,
                "tempo": 116.122,
                "valence": 0.89,
                "duration_ms": 160333.0,
                "key": 0.0,
                "mode": 1.0
            }
        }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint (preferred) - returns API status and model information
    """
    return {
        "status": "online",
        "message": "Music Release Year Prediction API",
        "model_loaded": model is not None,
        "model_path": str(MODEL_PATH),
        "features_required": feature_names if feature_names else [],
        "endpoints": {
            "root": "GET / (Interactive UI)",
            "health": "GET /health",
            "predict": "POST /predict",
            "docs": "GET /docs"
        }
    }


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def interactive_ui():
    """
    Serve interactive UI with sliders at root path
    """
    return FileResponse("static/index.html")


@app.post("/predict", tags=["Prediction"])
def predict_year(features: SongFeatures):
    """
    Predict the release year of a song based on audio features

    Returns the predicted year and confidence interval based on model RMSE
    """
    # Check if model is loaded
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure the model file exists."
        )

    try:
        # Convert Pydantic model to feature array in correct order
        feature_values = [
            features.acousticness,
            features.danceability,
            features.energy,
            features.instrumentalness,
            features.liveness,
            features.loudness,
            features.speechiness,
            features.tempo,
            features.valence,
            features.duration_ms,
            features.key,
            features.mode
        ]

        # Reshape for prediction
        input_data = np.array([feature_values])

        # Make prediction
        predicted_year = model.predict(input_data)[0]

        # Round to nearest year
        predicted_year = round(predicted_year)

        # Calculate confidence interval (±1 RMSE = ±14.69 years)
        confidence_interval = 14.69

        return {
            "predicted_year": int(predicted_year),
            "confidence_interval": {
                "lower": int(predicted_year - confidence_interval),
                "upper": int(predicted_year + confidence_interval)
            },
            "model_info": {
                "r2_score": 0.6804,
                "mae": 10.72,
                "rmse": 14.69
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
