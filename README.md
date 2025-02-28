# Offline Whisper

A lightweight Docker-based implementation of OpenAI's Whisper model for local speech recognition. This project provides a simple web interface for uploading audio files for transcription.

## Features

- Local deployment of OpenAI's Whisper model
- Web interface for audio file uploads
- Language selection directly in the web interface
- On-demand loading of different Whisper model sizes (tiny to large)
- Docker containerization for easy deployment
- Fully offline capable - no internet connection required after initial setup
- No data persistence - all audio files and transcriptions are deleted after processing

## Usage

### For End Users (Offline Usage)

The pre-built Docker image contains all Whisper models and can be used completely offline.

1. **Pull the Docker image** (requires internet connection once)

   ```bash
   docker pull ghcr.io/mgiesen/offline-whisper:latest
   ```

2. **Run the container** (works offline)

   ```bash
   docker run -d -p 8077:8077 ghcr.io/mgiesen/offline-whisper:latest
   ```

3. **Access the web interface** at `http://localhost:8077`

4. **Offline Deployment**

   You can export the Docker image to use it on offline systems:

   ```bash
   # Save the image to a file
   docker save ghcr.io/mgiesen/offline-whisper:latest > offline-whisper.tar

   # On the offline system
   docker load < offline-whisper.tar
   docker run -d -p 8077:8077 ghcr.io/mgiesen/offline-whisper:latest
   ```

### For Developers

If you want to modify the code before running the application, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/mgiesen/offline-whisper.git
   cd offline-whisper
   ```

2. **Build and start the containers** (development mode)

   ```bash
   docker-compose up -d
   ```

   Note: The development build doesn't preload models to save build time. Models will be downloaded on first use.

3. **Build for offline deployment** (includes all models)

   ```bash
   docker-compose -f docker-compose-deploy.yml up -d --build
   ```

4. **Access the web interface** at `http://localhost:8077`

## Web interface

![Image](readme/webapp.png)

## Important Notes

- The web interface lets you select from 5 different model sizes:

  - `tiny`: ~150MB - Fastest, lowest accuracy
  - `base`: ~150MB - Fast with decent accuracy
  - `small`: ~500MB - Good balance of speed and accuracy
  - `medium`: ~1.5GB - Better accuracy, slower
  - `large`: ~6GB - Best accuracy, slowest

- When you switch models, the previously loaded model is unloaded to free up memory
- Models are loaded on-demand (first transcription request) rather than at startup
- The pre-built Docker image includes all model files for offline use
- All uploaded audio files and generated transcripts are automatically deleted after processing for privacy
- No data is stored persistently - everything is processed in memory only

## Technical Details

### Development vs Deployment

- **Development Mode** (`docker-compose.yml`):

  - Faster builds, doesn't download models during build
  - Models are downloaded on first use (requires internet)
  - Ideal for code modifications and testing

- **Deployment Mode** (`docker-compose-deploy.yml`):
  - Includes all Whisper models in the image
  - Can be used completely offline
  - Larger image size (~8GB) but fully portable

## Acknowledgments

This project uses:

- [OpenAI Whisper](https://github.com/openai/whisper)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Nginx](https://nginx.org/)
