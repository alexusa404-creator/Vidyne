"""
AI Agent for conversational interactions with users
"""

import json
from typing import Dict, List, Optional, Any
from openai import OpenAI
from .utils import is_youtube_url, format_duration, format_file_size, get_openai_api_key


class AIAgent:
    """AI agent for conversational video download assistance"""
    
    def __init__(self):
        api_key = get_openai_api_key()
        if not api_key:
            print("⚠️  Warning: No OpenAI API key found. Set OPENAI_API_KEY environment variable for AI features.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.conversation_history = []
    
    def is_available(self) -> bool:
        """Check if AI agent is available (API key configured)"""
        return self.client is not None
    
    def greet_user(self, url: str) -> str:
        """Generate a greeting message and analyze the URL"""
        if not self.is_available():
            return self._fallback_greeting(url)
        
        try:
            platform = "YouTube" if is_youtube_url(url) else "this platform"
            
            prompt = f"""
            You are ClipGenius, a friendly AI assistant that helps users download videos. 
            
            The user has provided this URL: {url}
            
            Please:
            1. Greet the user warmly
            2. Identify what platform this appears to be from
            3. Briefly explain what you'll help them with
            4. Keep it conversational and helpful
            
            Keep the response concise but friendly.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            greeting = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": greeting})
            return greeting
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_greeting(url)
    
    def _fallback_greeting(self, url: str) -> str:
        """Fallback greeting when AI is not available"""
        platform = "YouTube" if is_youtube_url(url) else "this platform"
        return f"""
👋 Hello! I'm ClipGenius, your AI-powered video download assistant!

I see you want to download from {platform}. I'll help you:
• Analyze your video and show you the details
• Ask about your preferences (format, quality, etc.)
• Download exactly what you want
• Handle any issues that come up

Let's get started! 🚀
"""
    
    def summarize_video_metadata(self, video_info: Dict[str, Any]) -> str:
        """Summarize video metadata in a user-friendly way"""
        if not self.is_available():
            return self._fallback_video_summary(video_info)
        
        try:
            # Extract key information
            title = video_info.get('title', 'Unknown')
            uploader = video_info.get('uploader', 'Unknown')
            duration = video_info.get('duration', 0)
            view_count = video_info.get('view_count', 0)
            description = video_info.get('description', '')[:300] + '...' if video_info.get('description') else 'No description'
            
            prompt = f"""
            You are ClipGenius. Please create a friendly, conversational summary of this video:
            
            Title: {title}
            Uploader: {uploader}
            Duration: {format_duration(duration)}
            Views: {view_count:,} views
            Description: {description}
            
            Make it engaging and highlight the most interesting aspects. Keep it concise but informative.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": summary})
            return summary
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_video_summary(video_info)
    
    def _fallback_video_summary(self, video_info: Dict[str, Any]) -> str:
        """Fallback video summary when AI is not available"""
        title = video_info.get('title', 'Unknown')
        uploader = video_info.get('uploader', 'Unknown')
        duration = format_duration(video_info.get('duration'))
        view_count = video_info.get('view_count', 0)
        
        return f"""
📹 Video Details:
• Title: {title}
• Channel: {uploader}
• Duration: {duration}
• Views: {view_count:,} views

Ready to download! 🎬
"""
    
    def ask_about_preferences(self) -> str:
        """Ask user about their download preferences"""
        if not self.is_available():
            return self._fallback_preferences_question()
        
        try:
            prompt = """
            You are ClipGenius. Ask the user about their download preferences in a conversational way.
            
            Ask about:
            1. Video quality/format preferences
            2. Whether they want video or just audio
            3. If they want subtitles
            4. If they want thumbnails
            5. Custom filename preferences
            
            Make it feel like a natural conversation, not a formal questionnaire.
            Keep it friendly and helpful.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                temperature=0.7
            )
            
            question = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": question})
            return question
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_preferences_question()
    
    def _fallback_preferences_question(self) -> str:
        """Fallback preferences question when AI is not available"""
        return """
🎯 Let me know your preferences:

1. Do you want video + audio or just audio? (video/audio)
2. What quality do you prefer? (best/720p/480p/etc.)
3. Would you like subtitles? (yes/no)
4. Want to download the thumbnail too? (yes/no)
5. Any custom filename preference? (leave blank for default)

Just answer with your choices! 😊
"""
    
    def suggest_error_solution(self, error_message: str, url: str) -> str:
        """Suggest solutions for download errors"""
        if not self.is_available():
            return self._fallback_error_solution(error_message)
        
        try:
            prompt = f"""
            You are ClipGenius, helping a user who encountered this error while trying to download a video:
            
            Error: {error_message}
            URL: {url}
            
            Please:
            1. Explain what might have gone wrong in simple terms
            2. Suggest 2-3 practical solutions they can try
            3. Stay encouraging and helpful
            4. If it's a common issue, mention that
            
            Keep it conversational and supportive.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            suggestion = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": suggestion})
            return suggestion
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_error_solution(error_message)
    
    def _fallback_error_solution(self, error_message: str) -> str:
        """Fallback error solution when AI is not available"""
        return f"""
❌ Oops! Something went wrong: {error_message}

💡 Here are some things to try:
1. Check if the URL is correct and accessible
2. Try a different video quality/format
3. Make sure you have a stable internet connection
4. Some videos might be region-restricted or private

Don't worry, let's try again! 🔄
"""
    
    def offer_related_resources(self, video_info: Dict[str, Any]) -> str:
        """Offer to download related resources"""
        if not self.is_available():
            return self._fallback_resources_offer()
        
        try:
            has_subtitles = bool(video_info.get('subtitles') or video_info.get('automatic_captions'))
            has_thumbnail = bool(video_info.get('thumbnail'))
            
            prompt = f"""
            You are ClipGenius. The user just downloaded a video successfully.
            
            Available additional resources:
            - Subtitles: {'Available' if has_subtitles else 'Not available'}
            - Thumbnail: {'Available' if has_thumbnail else 'Not available'}
            
            Offer to download these additional resources in a friendly, conversational way.
            Don't be pushy - just let them know what's available.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            offer = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": offer})
            return offer
            
        except Exception as e:
            print(f"AI Error: {e}")
            return self._fallback_resources_offer()
    
    def _fallback_resources_offer(self) -> str:
        """Fallback resources offer when AI is not available"""
        return """
🎁 Great job! Your download is complete!

Would you also like to grab:
• Subtitles (if available)
• Video thumbnail
• Try another video?

Let me know what else you need! ✨
"""