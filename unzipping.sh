#!/bin/bash

# Directory where the zip files are located
zip_directory="./"

# Directory where the contents will be extracted
extract_directory="./takeout"


# Create the extraction directory if it doesn't exist
mkdir -p "$extract_directory"


# Loop through all zip files in the zip directory
for zip_file in "$zip_directory"/*.zip; do
  # Prompt for user confirmation before extracting each zip file
  read -p "Extract \"$zip_file\"? [Y/n] " choice

  # Convert the user's choice to lowercase using 'tr'
  choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')

  # Extract the zip file if the user confirms (Y or empty input)
  if [[ $choice == "y" || $choice == "" ]]; then
    7z x "$zip_file" -o"$extract_directory"
    echo "Extraction of \"$zip_file\" complete!"
  else
    echo "Skipping \"$zip_file\""
  fi
done

echo "All extractions complete!"