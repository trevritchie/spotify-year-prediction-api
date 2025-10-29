// Update slider value displays
const sliders = document.querySelectorAll('input[type="range"]');
sliders.forEach(slider => {
    const valueDisplay = document.getElementById(`${slider.id}-value`);

    slider.addEventListener('input', (e) => {
        const value = parseFloat(e.target.value);
        if (slider.id === 'duration_ms' || slider.id === 'key' || slider.id === 'mode') {
            valueDisplay.textContent = Math.round(value);
        } else {
            valueDisplay.textContent = value.toFixed(3);
        }
    });
});

// Example presets with actual song info
function load1920s() {
    setValues({
        acousticness: 0.982,
        danceability: 0.279,
        energy: 0.211,
        instrumentalness: 0.878,
        liveness: 0.665,
        loudness: -20.096,
        speechiness: 0.0366,
        tempo: 80.954,
        valence: 0.0594,
        duration_ms: 831667.0,
        key: 10.0,
        mode: 1.0
    });
}

function load1970s() {
    setValues({
        acousticness: 0.0936,
        danceability: 0.743,
        energy: 0.47,
        instrumentalness: 0.0000315,
        liveness: 0.186,
        loudness: -13.154,
        speechiness: 0.029,
        tempo: 116.122,
        valence: 0.89,
        duration_ms: 160333.0,
        key: 0.0,
        mode: 1.0
    });
}

function load2020() {
    setValues({
        acousticness: 0.221,
        danceability: 0.7,
        energy: 0.722,
        instrumentalness: 0.0,
        liveness: 0.272,
        loudness: -3.558,
        speechiness: 0.0369,
        tempo: 90.989,
        valence: 0.756,
        duration_ms: 140526.0,
        key: 7.0,
        mode: 0.0
    });
}

function setValues(values) {
    for (const [key, value] of Object.entries(values)) {
        const slider = document.getElementById(key);
        if (slider) {
            slider.value = value;
            const valueDisplay = document.getElementById(`${key}-value`);
            if (key === 'duration_ms' || key === 'key' || key === 'mode') {
                valueDisplay.textContent = Math.round(value);
            } else {
                valueDisplay.textContent = value.toFixed(3);
            }
        }
    }
}

// Form submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Hide previous results
    document.getElementById('result').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    // Gather all feature values
    const features = {
        acousticness: parseFloat(document.getElementById('acousticness').value),
        danceability: parseFloat(document.getElementById('danceability').value),
        energy: parseFloat(document.getElementById('energy').value),
        instrumentalness: parseFloat(document.getElementById('instrumentalness').value),
        liveness: parseFloat(document.getElementById('liveness').value),
        loudness: parseFloat(document.getElementById('loudness').value),
        speechiness: parseFloat(document.getElementById('speechiness').value),
        tempo: parseFloat(document.getElementById('tempo').value),
        valence: parseFloat(document.getElementById('valence').value),
        duration_ms: parseFloat(document.getElementById('duration_ms').value),
        key: parseFloat(document.getElementById('key').value),
        mode: parseFloat(document.getElementById('mode').value)
    };

    // Disable button while predicting
    const btn = document.querySelector('.predict-btn');
    btn.textContent = 'Predicting...';
    btn.disabled = true;

    try {
        // Call API
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(features)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();

        // Display results
        document.getElementById('predicted-year').textContent = result.predicted_year;
        document.getElementById('confidence-range').textContent =
            `${result.confidence_interval.lower} - ${result.confidence_interval.upper}`;
        document.getElementById('result').classList.remove('hidden');

    } catch (error) {
        // Display error
        document.getElementById('error-message').textContent =
            `Error: ${error.message}. Please try again.`;
        document.getElementById('error').classList.remove('hidden');
    } finally {
        // Re-enable button
        btn.textContent = 'Predict Release Year';
        btn.disabled = false;
    }
});

