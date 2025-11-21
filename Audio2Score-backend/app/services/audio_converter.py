"""
Audio to MIDI conversion service using Basic Pitch
"""
import os
import asyncio
from pathlib import Path
from typing import Tuple, Optional
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH


async def convert_audio_to_midi(audio_path: str) -> str:
    """
    Convert audio file to MIDI using Basic Pitch
    
    Args:
        audio_path: Path to the input audio file
        
    Returns:
        Path to the generated MIDI file
    """
    try:
        # Get output directory
        output_dir = os.path.dirname(audio_path)
        
        # Run conversion in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            _run_basic_pitch,
            audio_path,
            output_dir
        )
        
        # Basic Pitch creates files with _basic_pitch suffix
        audio_name = Path(audio_path).stem
        midi_path = os.path.join(output_dir, f"{audio_name}_basic_pitch.mid")
        
        if not os.path.exists(midi_path):
            raise FileNotFoundError(f"MIDI file not generated: {midi_path}")
        
        return midi_path
    
    except Exception as e:
        raise Exception(f"Audio to MIDI conversion failed: {str(e)}")


def _run_basic_pitch(audio_path: str, output_dir: str):
    """
    Run Basic Pitch conversion (blocking operation)
    """
    predict_and_save(
        [audio_path],
        output_dir,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False
    )


async def analyze_midi(midi_data: bytes) -> Tuple[Optional[float], Optional[int]]:
    """
    Analyze MIDI data to extract duration and note count
    
    Args:
        midi_data: MIDI file data as bytes
        
    Returns:
        Tuple of (duration in seconds, note count)
    """
    try:
        # Simple MIDI analysis
        # Count note-on events (0x90)
        note_count = 0
        for i in range(len(midi_data) - 2):
            # Check for note-on event with velocity > 0
            if (midi_data[i] & 0xF0) == 0x90 and midi_data[i + 2] > 0:
                note_count += 1
        
        # Duration estimation would require proper MIDI parsing
        # For now, return None for duration
        duration = None
        
        return duration, note_count
    
    except Exception as e:
        print(f"⚠️  MIDI analysis error: {str(e)}")
        return None, None


async def get_midi_info(midi_path: str) -> dict:
    """
    Get detailed information about a MIDI file
    
    Args:
        midi_path: Path to MIDI file
        
    Returns:
        Dictionary with MIDI information
    """
    try:
        # Read MIDI file
        with open(midi_path, 'rb') as f:
            midi_data = f.read()
        
        duration, note_count = await analyze_midi(midi_data)
        
        return {
            "size": len(midi_data),
            "duration": duration,
            "note_count": note_count
        }
    
    except Exception as e:
        print(f"⚠️  Error getting MIDI info: {str(e)}")
        return {
            "size": 0,
            "duration": None,
            "note_count": None
        }
