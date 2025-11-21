from chatterbox.mtl_tts import ChatterboxMultilingualTTS
import random
import numpy as np
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = None

def get_or_load_model():
    """Loads the ChatterboxMultilingualTTS model if it hasn't been loaded already,
    and ensures it's on the correct device."""

    global MODEL
    if MODEL is None:
        print("Model not loaded, initializing...")
        try:
            MODEL = ChatterboxMultilingualTTS.from_pretrained(DEVICE)
            if hasattr(MODEL, 'to') and str(MODEL.device) != DEVICE:
                MODEL.to(DEVICE)
            print(f"Model loaded successfully. Internal device: {getattr(MODEL, 'device', 'N/A')}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return MODEL

def set_seed(seed: int):
    """Sets the random seed for reproducibility across torch, numpy, and random."""
    torch.manual_seed(seed)
    if DEVICE == "cuda":
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)