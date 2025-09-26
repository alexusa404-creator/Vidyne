"""
Utility functions for ClipGenius
"""

import os
import re
from typing import Optional
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """Check if the provided string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_youtube_url(url: str) -> bool:
    """Check if URL is from YouTube"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    try:
        domain = urlparse(url).netloc.lower()
        return any(yt_domain in domain for yt_domain in youtube_domains)
    except Exception:
        return False


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage"""
    # Remove or replace characters that are problematic in filenames
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra whitespace and limit length
    filename = ' '.join(filename.split())[:200]
    return filename


def format_duration(seconds: Optional[int]) -> str:
    """Format duration in seconds to human readable format"""
    if seconds is None:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def format_file_size(bytes_size: Optional[int]) -> str:
    """Format file size in bytes to human readable format"""
    if bytes_size is None:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment variables"""
    return os.getenv('OPENAI_API_KEY')


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if it doesn't"""
    os.makedirs(path, exist_ok=True)