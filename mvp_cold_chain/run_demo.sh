#!/bin/bash

# Cold Chain Failure Prediction - Demo Launcher
# This script launches the interactive Streamlit dashboard

echo "=========================================="
echo "  Cold Chain Failure Prediction Demo"
echo "=========================================="
echo ""

# Check if data exists
if [ ! -f "data/processed/facilities_with_daily_weather_and_targets.csv" ]; then
    echo "⚠️  Data not found. Running data collection first..."
    echo ""
    python3 run_mvp.py
    echo ""
fi

echo "🚀 Starting interactive dashboard..."
echo ""
echo "📍 The app will open in your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit app
streamlit run app.py
