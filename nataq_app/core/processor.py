"""
Core Video Processing Engine - UPDATED
Handles video dubbing pipeline with pre-trained voices
Fixed: Complete speech synthesis (no truncation)
"""

import os
import whisper
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from TTS.api import TTS
from pydub import AudioSegment
import subprocess
import json
from datetime import datetime
from utils.config import (DEVICE, NLLB_MODEL, XTTS_MODEL, TEMP_DIR, 
                         OUTPUT_DIR, NLLB_LANG_CODES, MODELS_DIR, VOICES_DIR)
from core.dialect_translator import DialectTranslator
from core.subtitle_generator import SubtitleGenerator

# Pre-trained voice samples (embedded text for XTTS to use)
PRETRAINED_VOICES_TEXT = {
    "male": "مرحباً، أنا صوت ذكر عربي احترافي. يمكنني التحدث بوضوح وبطلاقة في اللغة العربية.",
    "female": "مرحباً، أنا صوت أنثى عربية احترافية. أستطيع التحدث بلهجة واضحة وطبيعية."
}

class VideoProcessor:
    """Handles the complete video dubbing pipeline"""
    
    def __init__(self):
        self.whisper_model = None
        self.nllb_model = None
        self.nllb_tokenizer = None
        self.tts_engine = None
        self.device = DEVICE
        
        # Dialect-specific translator
        self.dialect_translator = None
        
        # Subtitle generator
        self.subtitle_gen = SubtitleGenerator()
        
        # Pre-trained voice audio paths
        self.pretrained_voices = {
            "male": VOICES_DIR / "male_arabic.wav",
            "female": VOICES_DIR / "female_arabic.wav"
        }
        
        # Ensure voices directory exists
        VOICES_DIR.mkdir(parents=True, exist_ok=True)
    
    def load_whisper(self, model_name="medium", progress_callback=None):
        """Load Whisper model for speech recognition"""
        if progress_callback:
            progress_callback(5, f"Loading Whisper {model_name} model...")
        
        self.whisper_model = whisper.load_model(model_name, device=self.device)
        
        if progress_callback:
            progress_callback(10, f"✓ Whisper model loaded on {self.device}")
    
    def load_nllb(self, progress_callback=None):
        """Load NLLB-200 model for translation"""
        if progress_callback:
            progress_callback(15, "Loading NLLB-200 translation model...")
        
        self.nllb_tokenizer = AutoTokenizer.from_pretrained(
            NLLB_MODEL,
            cache_dir=str(MODELS_DIR)
        )
        self.nllb_model = AutoModelForSeq2SeqLM.from_pretrained(
            NLLB_MODEL,
            cache_dir=str(MODELS_DIR)
        ).to(self.device)
        
        if progress_callback:
            progress_callback(25, f"✓ NLLB-200 loaded on {self.device}")
    
    def load_tts(self, progress_callback=None):
        """Load XTTS v2 for voice synthesis"""
        if progress_callback:
            progress_callback(30, "Loading XTTS v2 voice synthesis model...")
        
        self.tts_engine = TTS(XTTS_MODEL).to(self.device)
        
        if progress_callback:
            progress_callback(35, f"✓ XTTS v2 loaded on {self.device}")
    
    def generate_pretrained_voice_sample(self, voice_type="male", progress_callback=None):
        """Generate pre-trained voice sample if it doesn't exist"""
        voice_path = self.pretrained_voices[voice_type]
        
        if voice_path.exists():
            if progress_callback:
                progress_callback(37, f"✓ Using existing {voice_type} voice sample")
            return str(voice_path)
        
        if progress_callback:
            progress_callback(36, f"Generating {voice_type} voice sample (one-time setup)...")
        
        # Generate sample using XTTS
        text = PRETRAINED_VOICES_TEXT[voice_type]
        
        # Use XTTS to generate with default Arabic voice
        self.tts_engine.tts_to_file(
            text=text,
            language="ar",
            file_path=str(voice_path)
        )
        
        if progress_callback:
            progress_callback(37, f"✓ {voice_type.capitalize()} voice sample generated")
        
        return str(voice_path)
    
    def extract_audio(self, video_path, progress_callback=None):
        """Extract audio from video using FFmpeg"""
        if progress_callback:
            progress_callback(40, "Extracting audio from video...")
        
        audio_path = TEMP_DIR / f"extracted_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM audio
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            str(audio_path)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        if progress_callback:
            progress_callback(45, f"✓ Audio extracted: {audio_path.name}")
        
        return str(audio_path)
    
    def transcribe_audio(self, audio_path, language, progress_callback=None):
        """Transcribe audio using Whisper"""
        if progress_callback:
            progress_callback(50, f"Transcribing audio in {language}...")
        
        result = self.whisper_model.transcribe(
            audio_path,
            language=language,
            task="transcribe",
            verbose=False
        )
        
        transcription = result["text"]
        segments = result.get("segments", [])
        
        if progress_callback:
            progress_callback(55, f"✓ Transcription completed: {len(transcription)} chars, {len(segments)} segments")
        
        return transcription, segments
    
    def translate_text(self, text, source_lang, target_lang, dialect=None, progress_callback=None):
        """
        Translate text using NLLB-200 with dialect support
        
        Args:
            text: Source text
            source_lang: Source language code
            target_lang: Target language code
            dialect: Arabic dialect (if target is Arabic)
            progress_callback: Progress function
        """
        if progress_callback:
            dialect_name = dialect if dialect else target_lang
            progress_callback(60, f"Translating {source_lang} → {target_lang} ({dialect_name})...")
        
        # If target is Arabic and dialect specified, use dialect translator
        if target_lang == "ar" and dialect and dialect != "msa":
            # Initialize dialect translator if not already done
            if not self.dialect_translator:
                if progress_callback:
                    progress_callback(61, "Loading dialect translation model...")
                self.dialect_translator = DialectTranslator(NLLB_MODEL, self.device)
            
            # Get NLLB source code
            src_code = NLLB_LANG_CODES.get(source_lang, "eng_Latn")
            
            # Translate to dialect
            translation = self.dialect_translator.translate_to_dialect(
                text, 
                src_code,
                dialect,
                progress_callback
            )
            
        else:
            # Standard translation (MSA or non-Arabic)
            # Get NLLB language codes
            src_code = NLLB_LANG_CODES.get(source_lang, "eng_Latn")
            tgt_code = NLLB_LANG_CODES.get(target_lang, "arb_Arab")
            
            # Split long text into chunks (max 512 tokens)
            sentences = text.split('. ')
            translations = []
            
            for i, sentence in enumerate(sentences):
                if not sentence.strip():
                    continue
                    
                # Tokenize
                inputs = self.nllb_tokenizer(
                    sentence,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=512
                ).to(self.device)
                
                # Force target language
                forced_bos_token_id = self.nllb_tokenizer.lang_code_to_id[tgt_code]
                
                # Translate
                with torch.no_grad():
                    outputs = self.nllb_model.generate(
                        **inputs,
                        forced_bos_token_id=forced_bos_token_id,
                        max_length=512,
                        num_beams=5
                    )
                
                sentence_translation = self.nllb_tokenizer.decode(outputs[0], skip_special_tokens=True)
                translations.append(sentence_translation)
                
                if progress_callback and i % 5 == 0:
                    progress = 60 + int((i / len(sentences)) * 5)
                    progress_callback(progress, f"Translating... {i+1}/{len(sentences)} sentences")
            
            translation = '. '.join(translations)
        
        if progress_callback:
            progress_callback(65, f"✓ Translation completed: {len(translation)} chars")
        
        return translation
    
    def synthesize_speech(self, text, voice_type="male", reference_audio=None, 
                         language="ar", dialect=None, progress_callback=None):
        """
        Generate speech using XTTS v2 with pre-trained or custom voice
        FIXED: Process ALL text completely with proper chunking
        """
        if progress_callback:
            progress_callback(70, f"Synthesizing speech with {voice_type} voice...")
        
        output_path = TEMP_DIR / f"synthesized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Determine reference audio for voice cloning
        if voice_type == "custom" and reference_audio and os.path.exists(reference_audio):
            speaker_wav = reference_audio
            use_speaker_wav = True
            if progress_callback:
                progress_callback(72, "Using custom voice cloning...")
        elif voice_type in ["male", "female"]:
            # Use pre-trained voice
            speaker_wav = str(self.pretrained_voices[voice_type])
            if not os.path.exists(speaker_wav):
                if progress_callback:
                    progress_callback(71, f"⚠️ Pre-trained {voice_type} voice not found!")
                    progress_callback(72, "Please run: python create_voices.py")
                raise FileNotFoundError(
                    f"Pre-trained {voice_type} voice not found at {speaker_wav}\n"
                    f"Run 'python create_voices.py' first to generate voices."
                )
            use_speaker_wav = True
            if progress_callback:
                progress_callback(72, f"Using pre-trained {voice_type} voice...")
        else:
            speaker_wav = None
            use_speaker_wav = False
            if progress_callback:
                progress_callback(72, "Using default TTS voice...")
        
        # Language code for XTTS
        lang_code = language if language in ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"] else "ar"
        
        # CRITICAL FIX: Better text chunking to avoid truncation
        # Split by sentences but keep reasonable chunk sizes
        import re
        
        # Split on sentence boundaries (., !, ?, ؟, .)
        sentences = re.split(r'[.!?؟。]\s+', text)
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        # Further chunk if sentences are too long (>200 chars)
        final_chunks = []
        for sent in sentences:
            if len(sent) > 200:
                # Split long sentences by commas or conjunctions
                parts = re.split(r'[,،;]\s+', sent)
                final_chunks.extend([p.strip() for p in parts if p.strip()])
            else:
                final_chunks.append(sent)
        
        if progress_callback:
            progress_callback(73, f"Processing {len(final_chunks)} text chunks...")
        
        audio_segments = []
        failed_chunks = 0
        
        for i, chunk in enumerate(final_chunks):
            if not chunk or len(chunk) < 3:
                continue
            
            temp_output = TEMP_DIR / f"temp_chunk_{i}_{datetime.now().strftime('%H%M%S')}.wav"
            
            try:
                # Generate audio for this chunk
                if use_speaker_wav and speaker_wav:
                    # Voice cloning mode
                    self.tts_engine.tts_to_file(
                        text=chunk,
                        speaker_wav=speaker_wav,
                        language=lang_code,
                        file_path=str(temp_output)
                    )
                else:
                    # Default voice mode
                    # Check if model has speakers
                    if hasattr(self.tts_engine, 'speakers') and self.tts_engine.speakers:
                        # Use first speaker as default
                        speaker = self.tts_engine.speakers[0]
                        self.tts_engine.tts_to_file(
                            text=chunk,
                            speaker=speaker,
                            language=lang_code,
                            file_path=str(temp_output)
                        )
                    else:
                        self.tts_engine.tts_to_file(
                            text=chunk,
                            language=lang_code,
                            file_path=str(temp_output)
                        )
                
                # Load audio segment
                if temp_output.exists() and temp_output.stat().st_size > 1000:
                    audio_segments.append(AudioSegment.from_wav(str(temp_output)))
                    
                    # Update progress
                    if progress_callback and (i % 3 == 0 or i == len(final_chunks) - 1):
                        progress = 73 + int((i / len(final_chunks)) * 7)
                        progress_callback(progress, f"Synthesized {i+1}/{len(final_chunks)} chunks")
                else:
                    failed_chunks += 1
                    if progress_callback:
                        progress_callback(73, f"⚠️ Chunk {i+1} produced no audio")
                
            except Exception as e:
                failed_chunks += 1
                if progress_callback:
                    progress_callback(73, f"⚠️ Failed chunk {i+1}: {str(e)[:50]}")
                continue
            
            finally:
                # Clean up temp file
                if temp_output.exists():
                    try:
                        temp_output.unlink()
                    except:
                        pass
        
        # Report if chunks failed
        if failed_chunks > 0 and progress_callback:
            progress_callback(78, f"⚠️ {failed_chunks}/{len(final_chunks)} chunks failed")
        
        # Combine all audio segments
        if audio_segments:
            if progress_callback:
                progress_callback(78, f"Combining {len(audio_segments)} audio segments...")
            
            combined = audio_segments[0]
            for segment in audio_segments[1:]:
                # Add small pause between chunks (150ms)
                silence = AudioSegment.silent(duration=150)
                combined = combined + silence + segment
            
            # Export combined audio
            combined.export(str(output_path), format="wav")
            
            if progress_callback:
                total_duration = len(combined) / 1000.0  # in seconds
                progress_callback(80, f"✓ Complete speech: {total_duration:.1f}s, {len(audio_segments)} segments")
        else:
            raise Exception("No audio segments were generated. Check TTS model and text input.")
        
        return str(output_path)
    
    def merge_audio_video(self, video_path, audio_path, progress_callback=None):
        """Merge new audio with video using FFmpeg"""
        if progress_callback:
            progress_callback(85, "Merging audio with video...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f"dubbed_{timestamp}.mp4"
        
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-i', str(audio_path),
            '-c:v', 'copy',  # Copy video stream
            '-c:a', 'aac',  # AAC audio codec
            '-b:a', '192k',  # Audio bitrate
            '-map', '0:v:0',  # Video from first input
            '-map', '1:a:0',  # Audio from second input
            '-shortest',  # Match shortest stream
            '-y',  # Overwrite
            str(output_path)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        if progress_callback:
            progress_callback(95, f"✓ Video merged: {output_path.name}")
        
        return str(output_path)
    
    def process_video(self, video_path, voice_type, reference_audio, source_lang, target_lang,
                     dialect, whisper_model, add_subtitles=True, progress_callback=None):
        """
        Complete video dubbing pipeline with subtitle support
        
        Args:
            video_path: Path to input video
            voice_type: "male", "female", or "custom"
            reference_audio: Path to custom voice (if voice_type == "custom")
            source_lang: Source language code
            target_lang: Target language code
            dialect: Arabic dialect (gulf, egyptian, levantine, north_african, msa)
            whisper_model: Whisper model size
            add_subtitles: Whether to add burned-in subtitles
            progress_callback: Function to report progress
        
        Returns:
            Path to dubbed video
        """
        try:
            # Load models
            self.load_whisper(whisper_model, progress_callback)
            self.load_nllb(progress_callback)
            self.load_tts(progress_callback)
            
            # Extract audio
            audio_path = self.extract_audio(video_path, progress_callback)
            
            # Transcribe
            transcription, segments = self.transcribe_audio(
                audio_path, source_lang, progress_callback
            )
            
            if progress_callback:
                progress_callback(57, f"Original text: {transcription[:100]}...")
            
            # Translate with dialect support
            translation = self.translate_text(
                transcription, source_lang, target_lang, dialect, progress_callback
            )
            
            if progress_callback:
                progress_callback(67, f"Translated text ({dialect}): {translation[:100]}...")
            
            # Synthesize speech (FIXED: complete synthesis)
            dubbed_audio = self.synthesize_speech(
                translation, voice_type, reference_audio, target_lang, dialect, progress_callback
            )
            
            # Merge audio and video
            temp_output = self.merge_audio_video(
                video_path, dubbed_audio, progress_callback
            )
            
            # Add subtitles if requested
            if add_subtitles:
                if progress_callback:
                    progress_callback(88, "Creating subtitles...")
                
                # Create SRT file
                srt_path = TEMP_DIR / f"subtitles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.srt"
                
                # Get video duration for subtitle timing
                duration = self.subtitle_gen.get_video_duration(video_path)
                
                # Create subtitles with Whisper segment timing if available
                if segments:
                    self.subtitle_gen.create_subtitles_with_timing(translation, segments, srt_path)
                else:
                    self.subtitle_gen.create_srt_file(translation, duration, srt_path)
                
                # Burn subtitles into video
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                final_output = OUTPUT_DIR / f"dubbed_subtitled_{timestamp}.mp4"
                
                self.subtitle_gen.burn_subtitles_into_video(
                    temp_output, srt_path, final_output, progress_callback=progress_callback
                )
                
                # Clean up temp video
                if os.path.exists(temp_output):
                    os.remove(temp_output)
                if os.path.exists(srt_path):
                    os.remove(srt_path)
                
                output_path = str(final_output)
            else:
                output_path = temp_output
            
            # Cleanup temporary files
            if progress_callback:
                progress_callback(98, "Cleaning up temporary files...")
            
            for temp_file in [audio_path, dubbed_audio]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            if progress_callback:
                progress_callback(100, "✅ Processing complete!")
            
            return output_path
            
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"❌ Error: {str(e)}")
            raise e
    
    def get_video_info(self, video_path):
        """Get video metadata using FFprobe"""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        info = json.loads(result.stdout)
        
        return info
