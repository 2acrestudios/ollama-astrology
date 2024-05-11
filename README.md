# Astrology Horoscope Generator Using Ollama

<img src="https://2acrestudios.com/wp-content/uploads/2024/05/00003-1748303672.png" align="right" style="width:300px;" />
This Python project is designed to generate personalized horoscopes based on astrological signs using a mix of modern and whole sign astrology. It leverages unique author styles, including those of popular authors, to create distinctive daily readings. The application can generate horoscopes for individual users, handle bulk generation from a CSV file, and create combined horoscopes for two individuals, reflecting on their synergy in a specified area of interest.

## Features

- **Personalized Horoscopes:** Generate daily readings based on the user's rising, sun, and moon signs.
- **Author Style Selection:** Choose from default or popular author styles for a unique flair in the horoscope presentations.
- **Batch Generation:** Supports generating horoscopes for multiple entries via a CSV file.
- **Dual Horoscopes:** Create a combined horoscope for two individuals, focusing on their interpersonal dynamics.
- **Error Handling:** Provides feedback for errors during horoscope generation, ensuring reliability.

## Requirements

Before running this project, ensure you have the following installed:
- Python 3.6 or higher
- `requests` library
- `tqdm` library for progress bars
- `termcolor` library for colored output
- `csv` module for handling CSV files
- Internet access to connect to the Ollama API for horoscope generation

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
