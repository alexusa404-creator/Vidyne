"""
Command-line interface for ClipGenius
"""

import os
import sys
import click
from colorama import init, Fore, Style
from typing import Optional, List
from .ai_agent import AIAgent
from .downloader import VideoDownloader
from .utils import is_valid_url, is_youtube_url


# Initialize colorama for cross-platform colored output
init(autoreset=True)


class CLIInterface:
    """Main CLI interface for ClipGenius"""
    
    def __init__(self):
        self.ai_agent = AIAgent()
        self.downloader = VideoDownloader()
        self.current_url: Optional[str] = None
        self.current_video_info: Optional[dict] = None
    
    def print_banner(self):
        """Print the ClipGenius banner"""
        banner = f"""
{Fore.CYAN}
╔═══════════════════════════════════════╗
║            🎬 ClipGenius 🤖            ║
║    AI-Powered Video Download Tool     ║
╚═══════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def print_success(self, message: str):
        """Print success message in green"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Print error message in red"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message in blue"""
        print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Print warning message in yellow"""
        print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input with colored prompt"""
        return input(f"{Fore.CYAN}❓ {prompt}{Style.RESET_ALL} ").strip()
    
    def validate_url(self, url: str) -> bool:
        """Validate and set the current URL"""
        if not is_valid_url(url):
            self.print_error("Invalid URL format. Please provide a valid video URL.")
            return False
        
        self.current_url = url
        return True
    
    def analyze_video(self) -> bool:
        """Analyze the video and get metadata"""
        if not self.current_url:
            return False
        
        self.print_info("Analyzing video... 🔍")
        
        # Get video information
        self.current_video_info = self.downloader.get_video_info(self.current_url)
        
        if not self.current_video_info:
            self.print_error("Could not extract video information. Please check the URL and try again.")
            return False
        
        return True
    
    def show_video_summary(self):
        """Display video summary using AI agent"""
        if not self.current_video_info:
            return
        
        print(f"\n{Fore.MAGENTA}🎬 Video Analysis{Style.RESET_ALL}")
        print("=" * 50)
        
        # Get AI summary
        summary = self.ai_agent.summarize_video_metadata(self.current_video_info)
        print(summary)
        print()
    
    def get_download_preferences(self) -> dict:
        """Get user's download preferences"""
        print(f"\n{Fore.YELLOW}📋 Download Preferences{Style.RESET_ALL}")
        print("=" * 50)
        
        # Ask AI agent for preferences
        preferences_prompt = self.ai_agent.ask_about_preferences()
        print(preferences_prompt)
        print()
        
        preferences = {}
        
        # Get format preference
        format_choice = self.get_user_input("Video or audio only? (video/audio)").lower()
        preferences['audio_only'] = format_choice.startswith('audio') or format_choice.startswith('a')
        
        # Get quality preference if not audio only
        if not preferences['audio_only']:
            quality = self.get_user_input("Quality preference? (best/720p/480p/360p/worst)")
            preferences['quality'] = quality if quality else 'best'
        
        # Get subtitles preference
        subtitles = self.get_user_input("Download subtitles? (yes/no)").lower()
        preferences['subtitles'] = subtitles.startswith('y')
        
        # Get thumbnail preference
        thumbnail = self.get_user_input("Download thumbnail? (yes/no)").lower()
        preferences['thumbnail'] = thumbnail.startswith('y')
        
        # Get custom filename
        custom_name = self.get_user_input("Custom filename? (leave blank for default)")
        preferences['custom_filename'] = custom_name if custom_name else None
        
        return preferences
    
    def show_available_formats(self):
        """Show available formats for the video"""
        if not self.current_url:
            return
        
        formats = self.downloader.get_available_formats(self.current_url)
        if not formats:
            self.print_warning("No formats available or could not fetch format information.")
            return
        
        print(f"\n{Fore.CYAN}📺 Available Formats{Style.RESET_ALL}")
        print("=" * 70)
        print(f"{'ID':<8} {'Resolution':<15} {'Extension':<8} {'Size':<12} {'Note'}")
        print("-" * 70)
        
        for fmt in formats[:10]:  # Show top 10 formats
            format_id = fmt.get('format_id', 'N/A')
            resolution = fmt.get('resolution', 'N/A')
            ext = fmt.get('ext', 'N/A')
            filesize = self._format_size(fmt.get('filesize'))
            note = fmt.get('format_note', '')[:20]
            
            print(f"{format_id:<8} {resolution:<15} {ext:<8} {filesize:<12} {note}")
        
        if len(formats) > 10:
            self.print_info(f"... and {len(formats) - 10} more formats available")
        print()
    
    def _format_size(self, size_bytes):
        """Format file size for display"""
        if size_bytes is None:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"
    
    def perform_download(self, preferences: dict):
        """Perform the actual download"""
        if not self.current_url:
            return
        
        print(f"\n{Fore.GREEN}🚀 Starting Download{Style.RESET_ALL}")
        print("=" * 50)
        
        # Perform main download
        result = self.downloader.download_video(
            url=self.current_url,
            audio_only=preferences.get('audio_only', False),
            custom_filename=preferences.get('custom_filename')
        )
        
        if result['success']:
            self.print_success(result['message'])
            
            # Download additional resources if requested
            if preferences.get('subtitles'):
                self.print_info("Downloading subtitles...")
                sub_result = self.downloader.download_subtitles(self.current_url)
                if sub_result['success']:
                    self.print_success("Subtitles downloaded!")
                else:
                    self.print_warning(f"Subtitles download failed: {sub_result['message']}")
            
            if preferences.get('thumbnail'):
                self.print_info("Downloading thumbnail...")
                thumb_result = self.downloader.download_thumbnail(self.current_url)
                if thumb_result['success']:
                    self.print_success("Thumbnail downloaded!")
                else:
                    self.print_warning(f"Thumbnail download failed: {thumb_result['message']}")
            
            # Offer related resources
            print(f"\n{Fore.MAGENTA}🎁 Additional Options{Style.RESET_ALL}")
            offer = self.ai_agent.offer_related_resources(self.current_video_info or {})
            print(offer)
            
        else:
            self.print_error(result['message'])
            
            # Get AI suggestions for the error
            print(f"\n{Fore.YELLOW}💡 Troubleshooting Help{Style.RESET_ALL}")
            suggestion = self.ai_agent.suggest_error_solution(result['error'], self.current_url)
            print(suggestion)
    
    def run_interactive_mode(self, url: str):
        """Run the interactive download process"""
        self.print_banner()
        
        # Validate URL
        if not self.validate_url(url):
            return False
        
        # Greet user and analyze URL
        greeting = self.ai_agent.greet_user(url)
        print(greeting)
        print()
        
        # Analyze video
        if not self.analyze_video():
            return False
        
        # Show video summary
        self.show_video_summary()
        
        # Ask if user wants to see available formats
        show_formats = self.get_user_input("Would you like to see available formats? (yes/no)").lower()
        if show_formats.startswith('y'):
            self.show_available_formats()
        
        # Get download preferences
        preferences = self.get_download_preferences()
        
        # Confirm download
        print(f"\n{Fore.CYAN}📋 Download Summary{Style.RESET_ALL}")
        print("=" * 50)
        print(f"URL: {self.current_url}")
        print(f"Type: {'Audio only' if preferences['audio_only'] else 'Video + Audio'}")
        if not preferences['audio_only']:
            print(f"Quality: {preferences.get('quality', 'best')}")
        print(f"Subtitles: {'Yes' if preferences['subtitles'] else 'No'}")
        print(f"Thumbnail: {'Yes' if preferences['thumbnail'] else 'No'}")
        if preferences['custom_filename']:
            print(f"Custom filename: {preferences['custom_filename']}")
        print()
        
        confirm = self.get_user_input("Proceed with download? (yes/no)").lower()
        if not confirm.startswith('y'):
            self.print_info("Download cancelled.")
            return False
        
        # Perform download
        self.perform_download(preferences)
        return True


@click.command()
@click.argument('url', required=True)
@click.option('--download-path', '-p', default='./downloads', 
              help='Directory to save downloads (default: ./downloads)')
@click.option('--audio-only', '-a', is_flag=True, 
              help='Download audio only')
@click.option('--quality', '-q', default='best',
              help='Video quality (best/worst/720p/480p/etc.)')
@click.option('--no-ai', is_flag=True,
              help='Skip AI interactions and use defaults')
def main(url: str, download_path: str, audio_only: bool, quality: str, no_ai: bool):
    """
    ClipGenius - AI-powered video downloader
    
    Download videos from YouTube and other platforms with AI assistance.
    
    Example: clipgenius https://www.youtube.com/watch?v=abc123
    """
    try:
        # Create CLI interface
        cli = CLIInterface()
        
        # Set custom download path if specified
        if download_path != './downloads':
            cli.downloader.download_path = download_path
            cli.downloader.ensure_directory(download_path)
        
        if no_ai:
            # Quick download without AI interaction
            cli.print_banner()
            cli.print_info(f"Quick download mode: {url}")
            
            if not cli.validate_url(url):
                sys.exit(1)
            
            if not cli.analyze_video():
                sys.exit(1)
            
            # Use provided options
            preferences = {
                'audio_only': audio_only,
                'quality': quality,
                'subtitles': False,
                'thumbnail': False,
                'custom_filename': None
            }
            
            cli.perform_download(preferences)
        else:
            # Interactive mode with AI
            success = cli.run_interactive_mode(url)
            if not success:
                sys.exit(1)
                
        cli.print_success("ClipGenius session completed! 🎉")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Download interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()