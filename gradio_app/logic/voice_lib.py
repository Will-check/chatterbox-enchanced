import json
import os
import shutil
import time

import gradio as gr
import numpy as np
import soundfile as sf

from pathlib import Path
from gradio_app.logic.common import DEFAULT_VOICE_LIBRARY, CONFIG_FILE

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    print("Warning: librosa not available - volume normalization will be disabled")
    LIBROSA_AVAILABLE = False

try:
    from scipy import signal
    SCIPY_AVAILABLE = True
except ImportError:
    print("Warning: scipy not available - advanced audio processing will be limited")
    SCIPY_AVAILABLE = False

    
def get_voice_profiles(voice_library_path):
    """Get list of saved voice profiles"""
    if not os.path.exists(voice_library_path):
        return []
    
    profiles = []
    for item in os.listdir(voice_library_path):
        profile_path = os.path.join(voice_library_path, item)
        if os.path.isdir(profile_path):
            config_file = os.path.join(profile_path, "config.json")
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    profiles.append({
                        'name': item,
                        'display_name': config.get('display_name', item),
                        'description': config.get('description', ''),
                        'config': config
                    })
                except:
                    continue
    return profiles

def get_voice_choices(voice_library_path):
    """Get voice choices for dropdown with display names"""
    profiles = get_voice_profiles(voice_library_path)
    choices = [("Manual Input (Upload Audio)", None)]
    for profile in profiles:
        display_text = f"🎭 {profile['display_name']} ({profile['name']})"
        choices.append((display_text, profile['name']))
    return choices

def refresh_voice_list(voice_library_path):
    """Refresh the voice profile list"""
    profiles = get_voice_profiles(voice_library_path)
    choices = [p['name'] for p in profiles]
    return gr.Dropdown(choices=choices, value=choices[0] if choices else None)

def refresh_voice_choices(voice_library_path):
    """Refresh voice choices for TTS dropdown"""
    choices = get_voice_choices(voice_library_path)
    return gr.Dropdown(choices=choices, value=None)

def get_audiobook_voice_choices(voice_library_path):
    """Get voice choices for audiobook creation (no manual input option)"""
    profiles = get_voice_profiles(voice_library_path)
    choices = []
    if not profiles:
        choices.append(("No voices available - Create voices first", None))
    else:
        for profile in profiles:
            display_text = f"🎭 {profile['display_name']} ({profile['name']})"
            choices.append((display_text, profile['name']))
    return choices

def refresh_audiobook_voice_choices(voice_library_path):
    """Refresh voice choices for audiobook creation"""
    choices = get_audiobook_voice_choices(voice_library_path)
    return gr.Dropdown(choices=choices, value=choices[0][1] if choices and choices[0][1] else None)

def ensure_voice_library_exists(voice_library_path):
    """Ensure the voice library directory exists"""
    Path(voice_library_path).mkdir(parents=True, exist_ok=True)
    return voice_library_path

def save_config(voice_library_path):
    """Save configuration including voice library path"""
    config = {
        'voice_library_path': voice_library_path,
        'last_updated': str(Path().resolve())  # timestamp
    }
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return f"✅ Configuration saved - Voice library path: {voice_library_path}"
    except Exception as e:
        return f"❌ Error saving configuration: {str(e)}"
    
def refresh_voice_list(voice_library_path):
    """Refresh the voice profile list"""
    profiles = get_voice_profiles(voice_library_path)
    choices = [p['name'] for p in profiles]
    return gr.update(choices=choices, value=choices[0] if choices else None)

def refresh_voice_choices(voice_library_path):
    """Refresh voice choices for TTS dropdown"""
    choices = get_voice_choices(voice_library_path)
    return gr.Dropdown(choices=choices, value=None)

def refresh_audiobook_voice_choices(voice_library_path):
    """Refresh voice choices for audiobook creation"""
    choices = get_audiobook_voice_choices(voice_library_path)
    return gr.Dropdown(choices=choices, value=choices[0][1] if choices and choices[0][1] else None)

def update_voice_library_path(new_path):
    """Update the voice library path and save to config"""
    if not new_path.strip():
        return DEFAULT_VOICE_LIBRARY, "❌ Path cannot be empty, using default", refresh_voice_list(DEFAULT_VOICE_LIBRARY), refresh_voice_choices(DEFAULT_VOICE_LIBRARY), refresh_audiobook_voice_choices(DEFAULT_VOICE_LIBRARY)
    
    # Ensure the directory exists
    ensure_voice_library_exists(new_path)
    
    # Save to config
    save_msg = save_config(new_path)
    
    # Return updated components
    return (
        new_path,  # Update the state
        save_msg,  # Status message
        refresh_voice_list(new_path),  # Updated voice dropdown
        # refresh_voice_choices(new_path),  # Updated TTS choices
        # refresh_audiobook_voice_choices(new_path)  # Updated audiobook choices
    )

def load_voice_profile(voice_library_path, voice_name):
    """Load a voice profile and return its settings"""
    if not voice_name:
        return None, 0.5, 0.5, 0.8, 0.05, 1.0, 1.2, "No voice selected"
    
    profile_dir = os.path.join(voice_library_path, voice_name)
    config_file = os.path.join(profile_dir, "config.json")
    
    if not os.path.exists(config_file):
        return None, 0.5, 0.5, 0.8, 0.05, 1.0, 1.2, f"❌ Voice profile '{voice_name}' not found"
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        audio_file = None
        if config.get('audio_file'):
            audio_path = os.path.join(profile_dir, config['audio_file'])
            if os.path.exists(audio_path):
                audio_file = audio_path
        
        return (
            audio_file,
            config.get('exaggeration', 0.5),
            config.get('cfg_weight', 0.5),
            config.get('temperature', 0.8),
            voice_name,
            config.get('display_name', ""),
            config.get('description', ""),
            f"✅ Loaded voice profile: {config.get('display_name', voice_name)} (v{config.get('version', '1.0')})"
        )
    except Exception as e:
        return None, 0.5, 0.5, 0.8, 0.05, 1.0, 1.2, f"❌ Error loading voice profile: {str(e)}"

def delete_voice_profile(voice_library_path, voice_name):
    """Delete a voice profile"""
    if not voice_name:
        return "❌ No voice selected", []
    
    profile_dir = os.path.join(voice_library_path, voice_name)
    if os.path.exists(profile_dir):
        try:
            shutil.rmtree(profile_dir)
            return f"✅ Voice profile '{voice_name}' deleted successfully!", get_voice_profiles(voice_library_path)
        except Exception as e:
            return f"❌ Error deleting voice profile: {str(e)}", get_voice_profiles(voice_library_path)
    else:
        return f"❌ Voice profile '{voice_name}' not found", get_voice_profiles(voice_library_path)

def analyze_audio_level(audio_data, sample_rate=24000):
    """
    Analyze the audio level and return various volume metrics.
    
    Args:
        audio_data: Audio array (numpy array)
        sample_rate: Sample rate of the audio
        
    Returns:
        dict: Dictionary with volume metrics
    """
    try:
        # Convert to numpy if it's a tensor
        if hasattr(audio_data, 'cpu'):
            audio_data = audio_data.cpu().numpy()
        
        # Ensure it's 1D
        if len(audio_data.shape) > 1:
            audio_data = audio_data.flatten()
        
        # RMS (Root Mean Square) level
        rms = np.sqrt(np.mean(audio_data**2))
        rms_db = 20 * np.log10(rms + 1e-10)  # Add small value to avoid log(0)
        
        # Peak level
        peak = np.max(np.abs(audio_data))
        peak_db = 20 * np.log10(peak + 1e-10)
        
        # LUFS (Loudness Units relative to Full Scale) - approximation
        # Apply K-weighting filter (simplified)
        try:
            if SCIPY_AVAILABLE:
                # High-shelf filter at 4kHz
                sos_high = signal.butter(2, 4000, 'highpass', fs=sample_rate, output='sos')
                filtered_high = signal.sosfilt(sos_high, audio_data)
                
                # High-frequency emphasis
                sos_shelf = signal.butter(2, 1500, 'highpass', fs=sample_rate, output='sos')
                filtered_shelf = signal.sosfilt(sos_shelf, filtered_high)
                
                # Mean square and convert to LUFS
                ms = np.mean(filtered_shelf**2)
                lufs = -0.691 + 10 * np.log10(ms + 1e-10)
            else:
                # Fallback if scipy not available
                lufs = rms_db
        except:
            # Fallback if filtering fails
            lufs = rms_db
        
        return {
            'rms_db': float(rms_db),
            'peak_db': float(peak_db),
            'lufs': float(lufs),
            'duration': len(audio_data) / sample_rate
        }
        
    except Exception as e:
        print(f"⚠️ Error analyzing audio level: {str(e)}")
        return {'rms_db': -40.0, 'peak_db': -20.0, 'lufs': -23.0, 'duration': 0.0}

def normalize_audio_to_target(audio_data, current_level_db, target_level_db, method='rms'):
    """
    Normalize audio to a target decibel level.
    
    Args:
        audio_data: Audio array to normalize
        current_level_db: Current level in dB
        target_level_db: Target level in dB
        method: Method to use ('rms', 'peak', or 'lufs')
        
    Returns:
        numpy.ndarray: Normalized audio data
    """
    try:
        # Convert to numpy if it's a tensor
        if hasattr(audio_data, 'cpu'):
            audio_data = audio_data.cpu().numpy()
        
        # Calculate gain needed
        gain_db = target_level_db - current_level_db
        gain_linear = 10 ** (gain_db / 20)
        
        # Apply gain with limiting to prevent clipping
        normalized_audio = audio_data * gain_linear
        
        # Soft limiting to prevent clipping
        max_val = np.max(np.abs(normalized_audio))
        if max_val > 0.95:  # Leave some headroom
            limiter_gain = 0.95 / max_val
            normalized_audio = normalized_audio * limiter_gain
            print(f"🔧 Applied soft limiting (gain: {limiter_gain:.3f}) to prevent clipping")
        
        return normalized_audio
        
    except Exception as e:
        print(f"⚠️ Error normalizing audio: {str(e)}")
        return audio_data

def save_voice_profile(voice_library_path, voice_name, display_name, description, audio_file, exaggeration, cfg_weight, temperature, enable_normalization=False, target_level_db=-18.0):
    """Save a voice profile with its settings and optional volume normalization"""
    if not voice_name:
        return "❌ Error: Voice name cannot be empty"
    
    # Sanitize voice name for folder
    safe_name = "".join(c for c in voice_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    
    if not safe_name:
        return "❌ Error: Invalid voice name"
    
    ensure_voice_library_exists(voice_library_path)
    
    profile_dir = os.path.join(voice_library_path, safe_name)
    os.makedirs(profile_dir, exist_ok=True)
    
    # Handle audio file and volume normalization
    audio_path = None
    normalization_applied = False
    original_level_info = None
    
    if audio_file:
        audio_ext = os.path.splitext(audio_file)[1]
        audio_path = os.path.join(profile_dir, f"reference{audio_ext}")
        
        # Apply volume normalization if enabled
        if enable_normalization:
            try:
                # Load and analyze original audio
                audio_data, sample_rate = librosa.load(audio_file, sr=24000)
                original_level_info = analyze_audio_level(audio_data, sample_rate)
                
                # Normalize audio
                normalized_audio = normalize_audio_to_target(
                    audio_data, 
                    original_level_info['rms_db'], 
                    target_level_db, 
                    method='rms'
                )
                
                # Save normalized audio
                sf.write(audio_path, normalized_audio, sample_rate)
                normalization_applied = True
                print(f"🎚️ Applied volume normalization: {original_level_info['rms_db']:.1f} dB → {target_level_db:.1f} dB")
                
            except Exception as e:
                print(f"⚠️ Volume normalization failed, using original audio: {str(e)}")
                # Fall back to copying original file
                shutil.copy2(audio_file, audio_path)
                normalization_applied = False
        else:
            # Copy original file without normalization
            shutil.copy2(audio_file, audio_path)
            
        # Store relative path
        audio_path = f"reference{audio_ext}"
    
    # Save configuration with normalization info and advanced parameters
    config = {
        "display_name": display_name or voice_name,
        "description": description or "",
        "audio_file": audio_path,
        "exaggeration": exaggeration,
        "cfg_weight": cfg_weight,
        "temperature": temperature,
        "created_date": str(time.time()),
        # Volume normalization settings
        "normalization_enabled": enable_normalization,
        "target_level_db": target_level_db,
        "normalization_applied": normalization_applied,
        "original_level_info": original_level_info,
    }
    
    config_file = os.path.join(profile_dir, "config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    # Prepare result message
    result_msg = f"✅ Voice profile '{display_name or voice_name}' saved successfully!"
    if original_level_info and normalization_applied:
        result_msg += f"\n📊 Audio normalized from {original_level_info['rms_db']:.1f} dB to {target_level_db:.1f} dB"
    elif original_level_info:
        result_msg += f"\n📊 Original audio level: {original_level_info['rms_db']:.1f} dB RMS"
    
    return result_msg