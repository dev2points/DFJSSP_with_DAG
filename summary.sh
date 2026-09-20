#!/bin/bash

# Configuration
PYTHON_SCRIPT="summary.py"
RESULTS_DIR="results"
SUMMARY_DIR="summary"

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "[X] Error: Python script '$PYTHON_SCRIPT' not found."
    exit 1
fi

# Ensure summary directory exists
mkdir -p "$SUMMARY_DIR"

echo "=========================================================="
echo "STARTING SUMMARY GENERATION (2 TO 4 FACTORIES)"
echo "=========================================================="

# Loop through factory counts from 2 to 4
for num_factories in {2..4}; do
    input_path="${RESULTS_DIR}/${num_factories}factories"
    output_csv="${SUMMARY_DIR}/${num_factories}factories.csv"

    # Check if the input directory exists
    if [ ! -d "$input_path" ]; then
        echo "[!] Directory $input_path does not exist, skipping..."
        continue
    fi

    echo ""
    echo "----------------------------------------------------------"
    echo "[>] Processing: $input_path -> $output_csv"
    echo "----------------------------------------------------------"

    # Execute summary python script
    python3 "$PYTHON_SCRIPT" "$input_path" "$output_csv"

    if [ $? -eq 0 ]; then
        echo "[✓] Successfully created: $output_csv"
    else
        echo "[X] Failed to process summary for: $input_path"
    fi
done

