#!/bin/bash

SOURCE_DIR="solution"
DEST_DIR="exercise"

# Remove destination if it exists
if [ -d "$DEST_DIR" ]; then
    rm -rf "$DEST_DIR"
fi

# Copy everything from solution to exercise
cp -r "$SOURCE_DIR" "$DEST_DIR"

# Process all .py files in the exercise directory
find "$DEST_DIR" -name "*.py" | while read -r file; do
    awk '
    BEGIN { inside=0; indent="" }
    $0 ~ /^[[:space:]]*# SOLUTION START --[[:space:]]*$/ {
        inside=1
        match($0, /^[[:space:]]*/)
        indent = substr($0, RSTART, RLENGTH)
        print indent "pass  # TODO: Place your code here!"
        next
    }
    $0 ~ /^[[:space:]]*# -- SOLUTION END[[:space:]]*$/ {
        inside=0
        next
    }
    inside == 0 { print }
    ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
done
