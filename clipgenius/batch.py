"""
Batch download functionality for ClipGenius
"""

import re
import requests
from typing import List, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from .utils import is_valid_url, is_youtube_url


class BatchDownloader:
    """Handles batch downloading by parsing webpages for video links"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_video_urls_from_webpage(self, webpage_url: str) -> List[str]:
        """Extract video URLs from a webpage"""
        try:
            response = self.session.get(webpage_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            video_urls = set()
            
            # Extract URLs from various sources
            video_urls.update(self._extract_from_links(soup, webpage_url))
            video_urls.update(self._extract_from_iframes(soup, webpage_url))
            video_urls.update(self._extract_from_text(response.text))
            
            # Filter and validate URLs
            valid_urls = []
            for url in video_urls:
                if is_valid_url(url) and self._is_video_url(url):
                    valid_urls.append(url)
            
            return list(set(valid_urls))  # Remove duplicates
            
        except Exception as e:
            print(f"Error extracting URLs from webpage: {str(e)}")
            return []
    
    def _extract_from_links(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Extract video URLs from anchor tags"""
        urls = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if self._is_video_url(full_url):
                urls.add(full_url)
        
        return urls
    
    def _extract_from_iframes(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Extract video URLs from iframe elements"""
        urls = set()
        
        for iframe in soup.find_all('iframe', src=True):
            src = iframe['src']
            full_url = urljoin(base_url, src)
            
            if self._is_video_url(full_url):
                urls.add(full_url)
        
        return urls
    
    def _extract_from_text(self, text: str) -> Set[str]:
        """Extract video URLs from plain text using regex"""
        urls = set()
        
        # Common video URL patterns
        patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://youtu\.be/[\w-]+',
            r'https?://(?:www\.)?vimeo\.com/\d+',
            r'https?://(?:www\.)?dailymotion\.com/video/[\w-]+',
            r'https?://(?:www\.)?twitch\.tv/videos/\d+',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            urls.update(matches)
        
        return urls
    
    def _is_video_url(self, url: str) -> bool:
        """Check if URL is likely a video URL"""
        if not is_valid_url(url):
            return False
        
        video_platforms = [
            'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
            'twitch.tv', 'tiktok.com', 'instagram.com', 'facebook.com',
            'twitter.com', 'x.com', 'rumble.com', 'bitchute.com'
        ]
        
        try:
            domain = urlparse(url).netloc.lower()
            return any(platform in domain for platform in video_platforms)
        except Exception:
            return False
    
    def parse_url_list(self, url_list_text: str) -> List[str]:
        """Parse a text containing multiple URLs (one per line or comma-separated)"""
        urls = []
        
        # Split by newlines and commas
        lines = url_list_text.replace(',', '\n').split('\n')
        
        for line in lines:
            line = line.strip()
            if line and is_valid_url(line):
                urls.append(line)
        
        return urls
    
    def suggest_filename(self, video_info: dict) -> str:
        """Suggest a custom filename based on video content"""
        title = video_info.get('title', 'unknown')
        uploader = video_info.get('uploader', 'unknown')
        duration = video_info.get('duration', 0)
        
        # Create a descriptive filename
        filename_parts = []
        
        if uploader and uploader.lower() != 'unknown':
            filename_parts.append(uploader[:20])  # Limit uploader name length
        
        if title and title.lower() != 'unknown':
            # Clean and truncate title
            clean_title = re.sub(r'[^\w\s-]', '', title)
            clean_title = ' '.join(clean_title.split())  # Remove extra whitespace
            filename_parts.append(clean_title[:50])  # Limit title length
        
        if duration and duration > 0:
            minutes = duration // 60
            if minutes > 60:
                hours = minutes // 60
                minutes = minutes % 60
                filename_parts.append(f"{hours}h{minutes}m")
            else:
                filename_parts.append(f"{minutes}m")
        
        suggested_name = " - ".join(filename_parts)
        
        # Fallback if nothing useful was found
        if not suggested_name or suggested_name.strip() == "":
            suggested_name = "video_download"
        
        return suggested_name