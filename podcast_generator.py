#!/usr/bin/env python3
"""
AI Podcast Generator
Generates a podcast script using LLM and converts it to audio using Eleven Labs TTS
"""

import argparse
import os
import sys
import re
from typing import List, Dict, Tuple
import openai
from elevenlabs import ElevenLabs
from pydub import AudioSegment
import io
from dotenv import load_dotenv


class PodcastGenerator:
    def __init__(self, llm_provider: str = "openai", llm_model: str = "gpt-3.5-turbo"):
        """Initialize the podcast generator with API clients"""
        # Load environment variables
        load_dotenv()
        
        # Validate API keys
        self.validate_api_keys()
        
        # Initialize LLM client
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        
        if llm_provider == "openai":
            self.openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif llm_provider == "grok":
            # For Grok, you would need to implement the specific API client
            # This is a placeholder - you'd need to adapt based on Grok's API
            self.openai_client = openai.OpenAI(
                api_key=os.getenv("GROK_API_KEY"),
                base_url="https://api.x.ai/v1"  # Grok's API endpoint
            )
        
        # Initialize Eleven Labs client
        self.elevenlabs_client = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY")
        )
        
        # Default voice IDs (you can replace these with your preferred voices)
        self.default_host_voice = "21m00Tcm4TlvDq8ikWAM"  # Rachel
        self.default_guest_voice = "AZnzlk1XvdvUeBnXmlld"  # Domi
    
    def validate_api_keys(self):
        """Validate that all required API keys are present"""
        required_keys = ["OPENAI_API_KEY", "ELEVENLABS_API_KEY"]
        
        # Check for Grok key if using Grok
        if hasattr(self, 'llm_provider') and self.llm_provider == "grok":
            required_keys.append("GROK_API_KEY")
        
        missing_keys = []
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ Error: Missing API keys in environment variables: {', '.join(missing_keys)}")
            print("Please ensure these keys are set in your .env file")
            sys.exit(1)
        
        print("✅ API keys validated successfully")
    
    def generate_script(self, topic: str) -> str:
        """Generate podcast script using LLM"""
        print(f"🎯 Generating script for topic: '{topic}'...")
        
        prompt = f"""Create a podcast script on the topic: "{topic}"

IMPORTANT REQUIREMENTS:
- The script must contain EXACTLY 3 exchanges from the HOST and EXACTLY 3 exchanges from the GUEST
- Total of 6 lines of dialogue
- Each line should be substantial (2-3 sentences)
- Format each line as either "HOST: [dialogue]" or "GUEST: [dialogue]"
- Make it conversational and engaging
- The HOST should introduce the topic and guide the conversation
- The GUEST should provide expertise and insights

Example format:
HOST: Welcome to our podcast! Today we're discussing [topic]. I'm excited to explore this fascinating subject with our expert guest.
GUEST: Thank you for having me! This is indeed a crucial topic that affects many aspects of our daily lives.
HOST: Let's dive right in. Can you explain the fundamental concepts behind [topic] for our listeners?
GUEST: Absolutely. The key thing to understand is that [topic] involves several interconnected elements that work together.
HOST: That's really insightful. What do you think the future holds for this field?
GUEST: I believe we're going to see significant developments in the coming years, particularly in areas like innovation and practical applications.

Now create a similar script for the topic: "{topic}"
"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a professional podcast script writer. Follow the format requirements exactly."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            script = response.choices[0].message.content.strip()
            print("✅ Script generated successfully")
            return script
            
        except Exception as e:
            print(f"❌ Error generating script: {str(e)}")
            sys.exit(1)
    
    def parse_script(self, script: str) -> List[Dict[str, str]]:
        """Parse the script into structured dialogue"""
        print("📝 Parsing script...")
        
        lines = script.strip().split('\n')
        dialogue = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Match HOST: or GUEST: prefixes
            if line.startswith("HOST:"):
                dialogue.append({
                    "speaker": "HOST",
                    "text": line[5:].strip()
                })
            elif line.startswith("GUEST:"):
                dialogue.append({
                    "speaker": "GUEST", 
                    "text": line[6:].strip()
                })
        
        # Validate we have exactly 6 lines (3 HOST, 3 GUEST)
        host_lines = [d for d in dialogue if d["speaker"] == "HOST"]
        guest_lines = [d for d in dialogue if d["speaker"] == "GUEST"]
        
        if len(host_lines) != 3 or len(guest_lines) != 3:
            print(f"❌ Error: Script parsing failed. Expected 3 HOST and 3 GUEST lines, got {len(host_lines)} HOST and {len(guest_lines)} GUEST lines")
            print("Raw script content:")
            print(script)
            sys.exit(1)
        #CHECK: Ensure we have exactly 6 dialogue lines
        if len(dialogue) != 6:
            print(f"❌ Error: Expected exactly 6 dialogue lines, got {len(dialogue)}")
            sys.exit(1)
        
        print(f"✅ Script parsed successfully: {len(host_lines)} HOST lines, {len(guest_lines)} GUEST lines")
        return dialogue
    
    def save_script(self, script: str, output_file: str):
        """Save the raw script to a text file"""
        print(f"💾 Saving script to {output_file}...")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(script)
            print(f"✅ Script saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving script: {str(e)}")
            sys.exit(1)
    
    def generate_audio_segment(self, text: str, voice_id: str, speaker: str) -> AudioSegment:
        """Generate audio for a single dialogue segment"""
        print(f"🎤 Converting {speaker} dialogue to speech...")
        
        try:
            # Generate audio using Eleven Labs
            audio_bytes = self.elevenlabs_client.generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            
            # Convert bytes to AudioSegment
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
            return audio_segment
            
        except Exception as e:
            print(f"❌ Error generating audio for {speaker}: {str(e)}")
            sys.exit(1)
    
    def generate_full_audio(self, dialogue: List[Dict[str, str]], host_voice: str, guest_voice: str) -> AudioSegment:
        """Generate complete podcast audio by combining all segments"""
        print("🎵 Generating complete podcast audio...")
        
        combined_audio = AudioSegment.empty()
        
        for i, line in enumerate(dialogue):
            speaker = line["speaker"]
            text = line["text"]
            voice_id = host_voice if speaker == "HOST" else guest_voice
            
            print(f"   Processing line {i+1}/6: {speaker}")
            
            # Generate audio for this line
            audio_segment = self.generate_audio_segment(text, voice_id, speaker)
            
            # Add a short pause between speakers (0.5 seconds)
            if i > 0:
                pause = AudioSegment.silent(duration=500)
                combined_audio += pause
            
            combined_audio += audio_segment
        
        print("✅ Complete audio generated successfully")
        return combined_audio
    
    def save_audio(self, audio: AudioSegment, output_file: str):
        """Save the combined audio to file"""
        print(f"💾 Saving audio to {output_file}...")
        
        try:
            # Determine format from file extension
            if output_file.lower().endswith('.wav'):
                audio.export(output_file, format="wav")
            elif output_file.lower().endswith('.mp3'):
                audio.export(output_file, format="mp3")
            else:
                # Default to mp3 if no valid extension
                output_file += '.mp3'
                audio.export(output_file, format="mp3")
            
            print(f"✅ Audio saved to {output_file}")
            
        except Exception as e:
            print(f"❌ Error saving audio: {str(e)}")
            sys.exit(1)
    
    def generate_podcast(self, topic: str, output_audio_file: str, output_script_file: str, 
                        host_voice: str, guest_voice: str):
        """Main method to generate complete podcast"""
        print("🎙️ Starting podcast generation...")
        print(f"Topic: {topic}")
        print(f"LLM Provider: {self.llm_provider}")
        print(f"LLM Model: {self.llm_model}")
        print(f"Host Voice: {host_voice}")
        print(f"Guest Voice: {guest_voice}")
        print("-" * 50)
        
        # Step 1: Generate script
        script = self.generate_script(topic)
        
        # Step 2: Save raw script
        self.save_script(script, output_script_file)
        
        # Step 3: Parse script
        dialogue = self.parse_script(script)
        
        # Step 4: Generate audio
        audio = self.generate_full_audio(dialogue, host_voice, guest_voice)
        
        # Step 5: Save audio
        self.save_audio(audio, output_audio_file)
        
        print("\n" + "=" * 50)
        print("🎉 Podcast generation completed successfully!")
        print(f"📄 Script saved to: {output_script_file}")
        print(f"🎵 Audio saved to: {output_audio_file}")
        print("=" * 50)


def main():

    print("Starting AI Podcast Generation...")

    """Main function to handle command line arguments and run the generator"""
    parser = argparse.ArgumentParser(description="AI Podcast Generator")
    
    # Required arguments
    parser.add_argument("--topic", "-t", required=True, help="Topic for the podcast")
    
    # Optional arguments with defaults
    parser.add_argument("--output_audio_file", "-a", default="podcast.mp3", 
                       help="Output audio file name (default: podcast.mp3)")
    parser.add_argument("--output_script_file", "-s", default="podcast_script.txt",
                       help="Output script file name (default: podcast_script.txt)")
    parser.add_argument("--llm_model", "-m", default="gpt-3.5-turbo",
                       help="LLM model to use (default: gpt-3.5-turbo)")
    parser.add_argument("--llm_provider", "-p", choices=["openai", "grok"], default="openai",
                       help="LLM provider to use (default: openai)")
    parser.add_argument("--host_voice", "-hv", default=None,
                       help="Eleven Labs Voice ID for Host")
    parser.add_argument("--guest_voice", "-gv", default=None,
                       help="Eleven Labs Voice ID for Guest")
    
    args = parser.parse_args()
    
    try:
        # Initialize generator
        generator = PodcastGenerator(
            llm_provider=args.llm_provider,
            llm_model=args.llm_model
        )
        
        # Use default voices if not specified
        host_voice = args.host_voice or generator.default_host_voice
        guest_voice = args.guest_voice or generator.default_guest_voice
        
        # Generate podcast
        generator.generate_podcast(
            topic=args.topic,
            output_audio_file=args.output_audio_file,
            output_script_file=args.output_script_file,
            host_voice=host_voice,
            guest_voice=guest_voice
        )
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()