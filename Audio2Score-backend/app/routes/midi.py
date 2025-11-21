"""
MIDI file routes
"""
import os
import base64
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, MidiFile
from app.schemas import MidiFileResponse, MidiLibraryResponse, MidiFileDetail
from app.auth import get_current_user
from app.services.audio_converter import convert_audio_to_midi, analyze_midi

router = APIRouter()


@router.post("/upload", response_model=MidiFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_audio(
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload audio file and convert to MIDI"""
    
    # Validate file type
    allowed_types = ["audio/mpeg", "audio/wav", "audio/mp3", "audio/x-wav", "audio/wave"]
    if audio.content_type not in allowed_types:
        if not audio.filename.lower().endswith(('.mp3', '.wav')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only MP3 and WAV files are supported"
            )
    
    # Create temporary directory for uploads
    os.makedirs("uploads", exist_ok=True)
    
    # Save uploaded file temporarily
    audio_path = f"uploads/audio_{current_user.id}_{audio.filename}"
    try:
        with open(audio_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        print(f"🎵 Converting {audio.filename} to MIDI...")
        
        # Convert audio to MIDI
        midi_path = await convert_audio_to_midi(audio_path)
        
        # Read MIDI file
        with open(midi_path, "rb") as f:
            midi_data = f.read()
        
        # Analyze MIDI
        duration, note_count = await analyze_midi(midi_data)
        
        # Store in database
        midi_file = MidiFile(
            user_id=current_user.id,
            filename=os.path.basename(midi_path),
            original_filename=audio.filename,
            midi_data=midi_data,
            duration=duration,
            note_count=note_count
        )
        
        db.add(midi_file)
        db.commit()
        db.refresh(midi_file)
        
        print(f"✅ MIDI file created: {midi_file.filename}")
        
        return MidiFileResponse.model_validate(midi_file)
    
    except Exception as e:
        print(f"❌ Error converting audio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to convert audio to MIDI: {str(e)}"
        )
    
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if 'midi_path' in locals() and os.path.exists(midi_path):
                os.remove(midi_path)
        except Exception as e:
            print(f"⚠️  Cleanup error: {str(e)}")


@router.get("/library", response_model=MidiLibraryResponse)
async def get_library(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's MIDI library"""
    
    midi_files = db.query(MidiFile).filter(
        MidiFile.user_id == current_user.id
    ).order_by(MidiFile.created_at.desc()).all()
    
    return MidiLibraryResponse(
        midis=[MidiFileResponse.model_validate(m) for m in midi_files],
        count=len(midi_files)
    )


@router.get("/{midi_id}", response_model=MidiFileDetail)
async def get_midi(
    midi_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific MIDI file with data"""
    
    midi_file = db.query(MidiFile).filter(
        MidiFile.id == midi_id,
        MidiFile.user_id == current_user.id
    ).first()
    
    if not midi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MIDI file not found"
        )
    
    # Convert MIDI data to base64
    midi_base64 = base64.b64encode(midi_file.midi_data).decode('utf-8')
    
    return {
        "id": midi_file.id,
        "filename": midi_file.filename,
        "original_filename": midi_file.original_filename,
        "duration": midi_file.duration,
        "note_count": midi_file.note_count,
        "created_at": midi_file.created_at,
        "midi_data": midi_base64
    }


@router.get("/{midi_id}/download")
async def download_midi(
    midi_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download MIDI file"""
    
    midi_file = db.query(MidiFile).filter(
        MidiFile.id == midi_id,
        MidiFile.user_id == current_user.id
    ).first()
    
    if not midi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MIDI file not found"
        )
    
    return Response(
        content=midi_file.midi_data,
        media_type="audio/midi",
        headers={
            "Content-Disposition": f'attachment; filename="{midi_file.original_filename}.mid"'
        }
    )


@router.delete("/{midi_id}")
async def delete_midi(
    midi_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a MIDI file"""
    
    midi_file = db.query(MidiFile).filter(
        MidiFile.id == midi_id,
        MidiFile.user_id == current_user.id
    ).first()
    
    if not midi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MIDI file not found"
        )
    
    db.delete(midi_file)
    db.commit()
    
    return {"message": "MIDI file deleted successfully"}
