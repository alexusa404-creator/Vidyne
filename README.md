# ClipGenius 🎬🤖

AI-powered command-line tool for downloading videos from YouTube and other platforms with conversational assistance.

## Features

- 🎯 **AI-Powered Interactions**: Conversational assistant that guides you through the download process
- 📱 **Multi-Platform Support**: Works with YouTube, Vimeo, and many other video platforms via yt-dlp
- 🎵 **Flexible Downloads**: Choose between video+audio, audio-only, or specific formats
- 📊 **Smart Analysis**: Get video metadata, duration, quality options before downloading
- 🎨 **Subtitle & Thumbnail Support**: Download subtitles and thumbnails alongside videos
- 🔧 **Error Handling**: AI-powered troubleshooting suggestions when downloads fail
- 🎪 **Interactive CLI**: Beautiful, colorful command-line interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/alexusa404-creator/Vidyne.git
cd Vidyne

# Install dependencies
pip install -r requirements.txt

# Install ClipGenius
pip install -e .
```

### Using virtual environment (recommended)

```bash
# Create virtual environment
python -m venv clipgenius-env

# Activate virtual environment
# On Windows:
clipgenius-env\Scripts\activate
# On macOS/Linux:
source clipgenius-env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Configuration

### OpenAI API Key (Optional but Recommended)

For AI-powered conversational features, you'll need an OpenAI API key:

1. Get your API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set it as an environment variable:

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# Windows
set OPENAI_API_KEY=your-api-key-here
```

3. Or create a `.env` file (copy from `.env.example`):

```env
OPENAI_API_KEY=your-api-key-here
```

**Note**: ClipGenius works without an API key, but you'll miss the AI conversational features.

## Usage

### Basic Usage

```bash
# Interactive mode with AI assistance
clipgenius "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Quick download without AI interaction
clipgenius "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --no-ai

# Audio only download
clipgenius "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio-only

# Custom download directory
clipgenius "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --download-path ~/Videos
```

### Advanced Options

```bash
# Specify video quality
clipgenius "URL" --quality 720p

# Run as Python module
python -m clipgenius "URL"

# Get help
clipgenius --help
```

### Interactive Experience

When you run ClipGenius in interactive mode, it will:

1. 🤖 **Greet you** and analyze your URL
2. 📊 **Show video details** (title, duration, channel, etc.)
3. 🎯 **Ask about preferences** (quality, format, subtitles, etc.)
4. 📺 **Display available formats** (if requested)
5. 🚀 **Download your video** with progress feedback
6. 🎁 **Offer additional resources** (subtitles, thumbnails)

## Examples

### Example 1: YouTube Video with AI

```bash
$ clipgenius "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

╔═══════════════════════════════════════╗
║            🎬 ClipGenius 🤖            ║
║    AI-Powered Video Download Tool     ║
╚═══════════════════════════════════════╝

👋 Hello! I'm ClipGenius, your AI assistant for video downloads!

I can see you want to download from YouTube. Let me analyze this video for you...

🎬 Video Analysis
==================================================
📹 "Rick Astley - Never Gonna Give You Up" by Rick Astley
⏱️  Duration: 3m 33s | 👀 1.4B views

This classic 80s hit has become an internet phenomenon! Ready to download this timeless track?

❓ Video or audio only? (video/audio) video
❓ Quality preference? (best/720p/480p/360p/worst) 720p
❓ Download subtitles? (yes/no) yes
❓ Download thumbnail? (yes/no) yes
❓ Custom filename? (leave blank for default) 

✅ Download completed successfully!
✅ Subtitles downloaded!
✅ Thumbnail downloaded!
```

### Example 2: Quick Audio Download

```bash
$ clipgenius "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio-only --no-ai

🎵 Quick audio download completed!
📁 Saved to: ./downloads/
```

## Supported Platforms

ClipGenius uses yt-dlp under the hood, supporting 1000+ websites including:

- YouTube
- Vimeo
- Twitch
- TikTok
- Instagram
- Twitter
- Facebook
- And many more!

## Project Structure

```
clipgenius/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for python -m clipgenius
├── cli.py               # Command-line interface and main logic
├── ai_agent.py          # AI conversational assistant
├── downloader.py        # Video downloading logic (yt-dlp wrapper)
└── utils.py             # Utility functions
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests (when available)
python -m pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Troubleshooting

### Common Issues

1. **"No OpenAI API key found"**
   - Set the OPENAI_API_KEY environment variable
   - Or use `--no-ai` flag to skip AI features

2. **"Could not extract video information"**
   - Check if the URL is correct and accessible
   - Some videos might be region-restricted or private
   - Try updating yt-dlp: `pip install --upgrade yt-dlp`

3. **Permission errors when downloading**
   - Make sure you have write permissions to the download directory
   - Try using a different download path with `--download-path`

### Getting Help

- Check the output of `clipgenius --help`
- Look at the error messages - ClipGenius provides helpful suggestions
- Open an issue on GitHub if you encounter bugs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the robust video downloading backend
- [OpenAI](https://openai.com/) for the conversational AI capabilities
- [Click](https://click.palletsprojects.com/) for the command-line interface framework