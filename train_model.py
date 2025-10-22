"""
train_model.py

Train a Random Forest Regressor to predict song release year
from Spotify audio features.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

def train_model():
    print("Loading Spotify dataset...")
    df = pd.read_csv('data/data.csv')

    # Extract year from release_date if needed
    if 'year' not in df.columns and 'release_date' in df.columns:
        df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

    # Select audio features for prediction
    feature_cols = [
        'acousticness', 'danceability', 'energy', 'instrumentalness',
        'liveness', 'loudness', 'speechiness', 'tempo', 'valence',
        'duration_ms', 'key', 'mode'
    ]

    # Filter available columns
    available_features = [col for col in feature_cols if col in df.columns]
    print(f"Using features: {available_features}")

    X = df[available_features]
    y = df['year']

    # Remove rows with missing target values
    valid_mask = y.notna()
    X = X[valid_mask]
    y = y[valid_mask]

    # Handle missing values in features
    X = X.fillna(X.mean())

    # Filter reasonable years (1900-2024)
    year_mask = (y >= 1900) & (y <= 2024)
    X = X[year_mask]
    y = y[year_mask]

    print(f"Total samples: {len(X)}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Train model
    print("\nTraining Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,  # Use all CPU cores
        verbose=1
    )
    model.fit(X_train, y_train)

    # Evaluate model
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"\n{'='*50}")
    print(f"Model Evaluation Metrics:")
    print(f"{'='*50}")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.2f} years")
    print(f"RMSE: {rmse:.2f} years")
    print(f"{'='*50}")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': available_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nTop 5 Most Important Features:")
    print(feature_importance.head())

    # Save model
    os.makedirs("models", exist_ok=True)
    model_path = "models/music_year_model.pkl"
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")

    # Save feature names for API
    joblib.dump(available_features, "models/feature_names.pkl")
    print("Feature names saved to models/feature_names.pkl")

if __name__ == "__main__":
    train_model()

