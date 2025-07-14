# AI Podcast Generator

A Python program that generates a short podcast by creating a script using a Large Language Model (LLM) and converting it to audio using Eleven Labs Text-to-Speech API.

## Features

- ✅ Generates podcast scripts with exactly 3 HOST and 3 GUEST exchanges (6 total lines)
- ✅ Supports OpenAI GPT models and Grok (with API access)
- ✅ Uses Eleven Labs for high-quality text-to-speech conversion
- ✅ Combines audio segments into a single podcast file
- ✅ Command-line interface with flexible options
- ✅ Robust error handling and informative feedback
- ✅ Secure API key management via environment variables

## Prerequisites

### System Requirements

1. **Python 3.8 or higher**
2. **FFmpeg** (required for audio processing)

#### Installing FFmpeg

**On macOS:**
```bash
brew install ffmpeg
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On Windows:**
- Download from https://ffmpeg.org/download.html
- Add to your system PATH

### API Keys Required

1. **OpenAI API Key**: Get from https://platform.openai.com/api-keys
2. **Eleven Labs API Key**: Get from https://elevenlabs.io/
3. **Grok API Key** (optional): Only if using Grok as LLM provider

## Setup Instructions

### Step 1: Clone/Download the Project

Create a new directory and save all the project files:

```bash
mkdir podcast_generator
cd podcast_generator
```

### Step 2: Set Up Python Environment

#### Option A: Using pyenv (Recommended)
```bash
# Install pyenv if you haven't already
curl https://pyenv.run | bash

# Install Python 3.9 (or your preferred version)
pyenv install 3.9.18
pyenv local 3.9.18

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Option B: Using system Python
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your API keys:
```bash
# OpenAI API Key
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Eleven Labs API Key  
ELEVENLABS_API_KEY=your-actual-elevenlabs-key-here

# Grok API Key (optional)
GROK_API_KEY=your-actual-grok-key-here
```

### Step 5: Verify Setup

Test that everything is working:
```bash
python podcast_generator.py --help
```

## Usage

### Basic Usage

Generate a podcast with default settings:
```bash
python podcast_generator.py --topic "The Future of Artificial Intelligence"
```

This will create:
- `podcast_script.txt` - The generated script
- `podcast.mp3` - The audio file

### Advanced Usage

#### Custom Output Files
```bash
python podcast_generator.py \
    --topic "Climate Change Solutions" \
    --output_audio_file "climate_podcast.wav" \
    --output_script_file "climate_script.txt"
```

#### Different LLM Models
```bash
python podcast_generator.py \
    --topic "Quantum Computing Basics" \
    --llm_model "gpt-4" \
    --llm_provider "openai"
```

#### Custom Voices
```bash
python podcast_generator.py \
    --topic "Space Exploration" \
    --host_voice "21m00Tcm4TlvDq8ikWAM" \
    --guest_voice "AZnzlk1XvdvUeBnXmlld"
```

#### Using Grok (if available)
```bash
python podcast_generator.py \
    --topic "Renewable Energy" \
    --llm_provider "grok"
```

### Command Line Options

| Option | Short | Required | Default | Description |
|--------|-------|----------|---------|-------------|
| `--topic` | `-t` | Yes | - | Topic for the podcast |
| `--output_audio_file` | `-a` | No | `podcast.mp3` | Output audio file name |
| `--output_script_file` | `-s` | No | `podcast_script.txt` | Output script file name |
| `--llm_model` | `-m` | No | `gpt-3.5-turbo` | LLM model to use |
| `--llm_provider` | `-p` | No | `openai` | LLM provider (`openai` or `grok`) |
| `--host_voice` | `-hv` | No | Rachel | Eleven Labs Voice ID for Host |
| `--guest_voice` | `-gv` | No | Domi | Eleven Labs Voice ID for Guest |

## Finding Voice IDs

To use custom voices from Eleven Labs:

1. Go to https://elevenlabs.io/
2. Navigate to Voice Library
3. Find a voice you like
4. Copy the Voice ID from the URL or voice details

Common Voice IDs:
- Rachel (Female): `21m00Tcm4TlvDq8ikWAM`
- Domi (Female): `AZnzlk1XvdvUeBnXmlld`
- Josh (Male): `TxGEqnHWrfWFTfGW9XjX`
- Arnold (Male): `VR6AewLTigWG4xSOukaG`

## Project Structure

```
podcast_generator/
├── .env                  # Your API keys (create from .env.example)
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
├── podcast_generator.py  # Main script
├── README.md            # This file
├── venv/                # Virtual environment (created during setup)
├── podcast_script.txt   # Generated script (created when run)
└── podcast.mp3          # Generated audio (created when run)
```

## Troubleshooting

### Common Issues

1. **"Missing API keys" error**
   - Check that your `.env` file exists and has correct keys
   - Ensure no extra spaces around the `=` sign

2. **"FFmpeg not found" error**
   - Install FFmpeg using the instructions above
   - Restart your terminal after installation

3. **"Script parsing failed" error**
   - The LLM didn't follow the exact format
   - Try running again, or try a different model

4. **"Audio generation failed" error**
   - Check your Eleven Labs API key
   - Verify voice IDs are correct
   - Check your API quota

5. **"Permission denied" when saving files**
   - Make sure you have write permissions in the directory
   - Try running from a different directory

### Getting Help

If you encounter issues:
1. Check the error message carefully
2. Verify all prerequisites are installed
3. Check your API keys and quotas
4. Try with a simpler topic first

## Example Output

After running successfully, you'll see output like:
```
✅ API keys validated successfully
🎯 Generating script for topic: 'The Future of AI'...
✅ Script generated successfully
💾 Saving script to podcast_script.txt...
✅ Script saved to podcast_script.txt
📝 Parsing script...
✅ Script parsed successfully: 3 HOST lines, 3 GUEST lines
🎵 Generating complete podcast audio...
   Processing line 1/6: HOST
🎤 Converting HOST dialogue to speech...
   Processing line 2/6: GUEST
🎤 Converting GUEST dialogue to speech...
   ... (continues for all 6 lines)
✅ Complete audio generated successfully
💾 Saving audio to podcast.mp3...
✅ Audio saved to podcast.mp3

==================================================
🎉 Podcast generation completed successfully!
📄 Script saved to: podcast_script.txt
🎵 Audio saved to: podcast.mp3
==================================================
```

## License

This project is for educational purposes. Please respect the terms of service of OpenAI and Eleven Labs APIs.