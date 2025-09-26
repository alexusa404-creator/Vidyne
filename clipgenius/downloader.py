"""
Video downloader module using yt-dlp
"""

import os
import yt_dlp
from typing import Dict, List, Optional, Any
from .utils import sanitize_filename, ensure_directory


class VideoDownloader:
    """Handles video/audio downloading using yt-dlp"""
    
    def __init__(self, download_path: str = "./downloads"):
        self.download_path = download_path
        ensure_directory(download_path)
        
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            print(f"Error extracting video info: {str(e)}")
            return None
    
    def get_available_formats(self, url: str) -> List[Dict[str, Any]]:
        """Get available formats for the video"""
        info = self.get_video_info(url)
        if not info:
            return []
        
        formats = info.get('formats', [])
        # Filter and organize formats
        organized_formats = []
        
        for fmt in formats:
            format_info = {
                'format_id': fmt.get('format_id'),
                'ext': fmt.get('ext'),
                'resolution': fmt.get('resolution', 'audio only' if fmt.get('vcodec') == 'none' else 'unknown'),
                'filesize': fmt.get('filesize'),
                'acodec': fmt.get('acodec'),
                'vcodec': fmt.get('vcodec'),
                'format_note': fmt.get('format_note', ''),
                'quality': fmt.get('quality', 0)
            }
            organized_formats.append(format_info)
        
        # Sort by quality (higher is better)
        organized_formats.sort(key=lambda x: x['quality'] or 0, reverse=True)
        return organized_formats
    
    def download_video(self, url: str, format_id: Optional[str] = None, 
                      audio_only: bool = False, custom_filename: Optional[str] = None) -> Dict[str, Any]:
        """Download video with specified options"""
        
        # Build yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'ignoreerrors': False,
        }
        
        if custom_filename:
            safe_filename = sanitize_filename(custom_filename)
            ydl_opts['outtmpl'] = os.path.join(self.download_path, f'{safe_filename}.%(ext)s')
        
        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_id:
            ydl_opts['format'] = format_id
        else:
            ydl_opts['format'] = 'best'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                return {
                    'success': True,
                    'message': 'Download completed successfully!',
                    'path': self.download_path
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Download failed: {str(e)}'
            }
    
    def download_subtitles(self, url: str, languages: List[str] = None) -> Dict[str, Any]:
        """Download subtitles for the video"""
        if languages is None:
            languages = ['en', 'auto']
        
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': languages,
            'skip_download': True,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                return {
                    'success': True,
                    'message': 'Subtitles downloaded successfully!',
                    'path': self.download_path
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Subtitle download failed: {str(e)}'
            }
    
    def download_thumbnail(self, url: str) -> Dict[str, Any]:
        """Download video thumbnail"""
        ydl_opts = {
            'writethumbnail': True,
            'skip_download': True,
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                return {
                    'success': True,
                    'message': 'Thumbnail downloaded successfully!',
                    'path': self.download_path
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Thumbnail download failed: {str(e)}'
            }