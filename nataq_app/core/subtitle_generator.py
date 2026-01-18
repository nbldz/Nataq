"""
Subtitle Generator Module
Creates burned-in subtitles for deaf/hard-of-hearing accessibility
Supports Arabic RTL text rendering
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime
import textwrap

class SubtitleGenerator:
    """Handles subtitle generation and burning into video"""
    
    def __init__(self):
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def create_srt_file(self, text, duration, output_path, max_chars_per_line=50):
        """
        Create SRT subtitle file from translated text
        
        Args:
            text: Translated text
            duration: Video duration in seconds
            output_path: Path to save SRT file
            max_chars_per_line: Maximum characters per subtitle line
        
        Returns:
            Path to created SRT file
        """
        
        # Split text into sentences
        import re
        sentences = re.split(r'[.!?؟。]\s*', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate timing for each subtitle
        time_per_sentence = duration / len(sentences) if sentences else duration
        
        srt_content = []
        current_time = 0
        
        for i, sentence in enumerate(sentences, 1):
            # Wrap long sentences
            wrapped_lines = textwrap.wrap(sentence, width=max_chars_per_line)
            subtitle_text = '\n'.join(wrapped_lines)
            
            # Calculate start and end time
            start_time = current_time
            end_time = current_time + time_per_sentence
            
            # Format timestamps (HH:MM:SS,mmm)
            start_ts = self._format_timestamp(start_time)
            end_ts = self._format_timestamp(end_time)
            
            # Add SRT entry
            srt_content.append(f"{i}")
            srt_content.append(f"{start_ts} --> {end_ts}")
            srt_content.append(subtitle_text)
            srt_content.append("")  # Blank line between entries
            
            current_time = end_time
        
        # Write SRT file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        return output_path
    
    def _format_timestamp(self, seconds):
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def burn_subtitles_into_video(self, video_path, srt_path, output_path, 
                                   subtitle_style=None, progress_callback=None):
        """
        Burn subtitles permanently into video using FFmpeg
        SIMPLIFIED: Use SRT directly for better Windows compatibility
        """
        
        if progress_callback:
            progress_callback(90, "Burning subtitles into video...")
        
        # Use SRT directly with subtitles filter (works better on Windows)
        # Convert path to use forward slashes
        srt_path_ffmpeg = str(srt_path).replace('\\', '/').replace(':', '\\:')
        
        # FFmpeg command using subtitles filter with SRT
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f"subtitles='{srt_path_ffmpeg}':force_style='FontName=Arial,FontSize=20,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Bold=1,Outline=2,Shadow=2,Alignment=2,MarginV=20'",
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-c:a', 'copy',
            '-y',
            str(output_path)
        ]
        
        if progress_callback:
            progress_callback(92, "Processing video with subtitles...")
        
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # If subtitles filter fails, try without force_style
            if progress_callback:
                progress_callback(91, "Retrying with basic subtitles...")
            
            cmd_simple = [
                'ffmpeg',
                '-i', str(video_path),
                '-vf', f"subtitles='{srt_path_ffmpeg}'",
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-c:a', 'copy',
                '-y',
                str(output_path)
            ]
            
            result = subprocess.run(cmd_simple, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg subtitle burning failed: {result.stderr}")
        
        if progress_callback:
            progress_callback(95, "✓ Subtitles burned into video")
        
        return output_path
    
    def _convert_srt_to_ass(self, srt_path, ass_path, style):
        """
        Convert SRT to ASS format with custom styling
        ASS format better supports Arabic RTL text
        """
        
        # Read SRT content
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        
        # Parse SRT entries
        entries = self._parse_srt(srt_content)
        
        # Create ASS content
        ass_content = self._create_ass_header(style)
        
        # Add dialogue entries
        for entry in entries:
            start = entry['start']
            end = entry['end']
            text = entry['text'].replace('\n', '\\N')  # ASS line break
            
            # ASS dialogue format
            dialogue = f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
            ass_content += dialogue
        
        # Write ASS file
        with open(ass_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)
        
        return ass_path
    
    def _parse_srt(self, srt_content):
        """Parse SRT content into structured entries"""
        entries = []
        blocks = srt_content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                # Parse timestamp line
                time_line = lines[1]
                start_str, end_str = time_line.split(' --> ')
                
                # Convert SRT timestamp to ASS timestamp
                start = self._srt_to_ass_time(start_str)
                end = self._srt_to_ass_time(end_str)
                
                # Get subtitle text
                text = '\n'.join(lines[2:])
                
                entries.append({
                    'start': start,
                    'end': end,
                    'text': text
                })
        
        return entries
    
    def _srt_to_ass_time(self, srt_time):
        """Convert SRT timestamp to ASS timestamp"""
        # SRT: HH:MM:SS,mmm
        # ASS: H:MM:SS.cc (centiseconds)
        time_part, millis_part = srt_time.split(',')
        h, m, s = time_part.split(':')
        cs = int(millis_part) // 10  # Convert milliseconds to centiseconds
        
        return f"{int(h)}:{m}:{s}.{cs:02d}"
    
    def _create_ass_header(self, style):
        """Create ASS file header with styling"""
        
        header = f"""[Script Info]
Title: Nataq Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style['font']},{style['font_size']},{style['primary_color']},&H000000FF,{style['outline_color']},{style['back_color']},{style['bold']},{style['italic']},0,0,100,100,0,0,{style['border_style']},{style['outline']},{style['shadow']},{style['alignment']},10,10,{style['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        return header
    
    def create_subtitles_with_timing(self, text, segments, output_path):
        """
        Create SRT file using Whisper segments for precise timing
        
        Args:
            text: Full translated text
            segments: Whisper segments with timestamps
            output_path: Output SRT path
        """
        
        # If we have Whisper segments, use them for timing
        if segments:
            return self._create_srt_from_segments(text, segments, output_path)
        else:
            # Fallback to duration-based splitting
            return self.create_srt_file(text, 0, output_path)
    
    def _create_srt_from_segments(self, translated_text, segments, output_path):
        """Create SRT using Whisper segment timing"""
        
        # Split translated text into parts matching number of segments
        import re
        sentences = re.split(r'[.!?؟。]\s*', translated_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Match sentences to segments (approximate)
        srt_content = []
        
        for i, segment in enumerate(segments):
            # Get corresponding translated sentence
            if i < len(sentences):
                subtitle_text = sentences[i]
            else:
                # If more segments than sentences, reuse last sentence
                subtitle_text = sentences[-1] if sentences else ""
            
            start_time = segment.get('start', 0)
            end_time = segment.get('end', start_time + 2)
            
            # Format timestamps
            start_ts = self._format_timestamp(start_time)
            end_ts = self._format_timestamp(end_time)
            
            # Add SRT entry
            srt_content.append(f"{i+1}")
            srt_content.append(f"{start_ts} --> {end_ts}")
            srt_content.append(subtitle_text)
            srt_content.append("")
        
        # Write SRT file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        return output_path
    
    def get_video_duration(self, video_path):
        """Get video duration using FFprobe"""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            duration = float(result.stdout.strip())
            return duration
        except:
            return 0
