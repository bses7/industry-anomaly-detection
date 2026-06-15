import os
import torch
import torchaudio
import argparse
import yaml
import numpy as np
import librosa

# Import custom modules
from src.data.preprocessing import AudioTransform
from src.models.vae import VAE
from src.models.vit import ViT
# Assuming you saved the hybrid version in hybrid.py as discussed
from src.models.hybrid import ViT as HybridViT
from src.utils.visualizations import get_base64_visual


# --- CONFIGURATION & MODEL REGISTRY ---
MODEL_DIR = "experiments"
MODEL_REGISTRY = {
    "fan":    {"path": "vit_fan_0dB.pth",    "class": ViT},
    "pump":   {"path": "vit_pump_0dB.pth",   "class": ViT},
    "valve":  {"path": "hybrid_valve_0dB.pth", "class": HybridViT},
    "slider": {"path": "vae_slider_0dB.pth",  "class": VAE}
}

def load_trained_model(machine_type, device):
    """Dynamically loads the correct model architecture and weights."""
    machine_type = machine_type.lower().strip()
    
    if machine_type not in MODEL_REGISTRY:
        raise ValueError(f"Machine type '{machine_type}' not supported.")
    
    reg = MODEL_REGISTRY[machine_type]
    model_path = os.path.join(MODEL_DIR, reg["path"])
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    # --- ARCHITECTURE INITIALIZATION ---
    if machine_type == "slider":
        # Standard VAE parameters
        model = reg["class"](latent_dim=128)
        
    elif machine_type == "valve":
        # Valve MUST match the Hybrid parameters from config.yaml
        model = reg["class"](
            latent_dim=256, 
            embed_dim=384, 
            depth=4,   # <--- Match your 'Hybrid' training run
            heads=12   # <--- Match your 'Hybrid' training run
        )
        
    else: # fan and pump
        # Standard ViT parameters
        model = reg["class"](
            latent_dim=256, 
            embed_dim=384, 
            depth=6,   # <--- Match your 'ViT' training run
            heads=12
        )

    # Load weights
    try:
        # map_location handles moving from Kaggle GPU to your PC CPU/GPU
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        return model
    except Exception as e:
        print(f"FAILED TO LOAD {machine_type.upper()} MODEL: {str(e)}")
        raise e
    
def predict(audio_path, machine_type):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    waveform, sr = librosa.load(audio_path, sr=16000)
    waveform = torch.from_numpy(waveform).unsqueeze(0)
    
    transform = AudioTransform()
    spec = transform(waveform).unsqueeze(0).to(device)
    
    model = load_trained_model(machine_type, device)
    
    with torch.no_grad():
        recon, mu, logvar = model(spec)
        mse = torch.mean(torch.pow(spec - recon, 2)).item()
        anomaly_score = np.log10(mse + 1e-10)
    
    visual_b64 = get_base64_visual(spec, recon)
        
    return anomaly_score, mse, visual_b64

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Industrial Acoustic Anomaly Detection Inference")
    parser.add_argument("--file", type=str, required=True, help="Path to .wav file")
    parser.add_argument("--type", type=str, required=True, choices=["fan", "pump", "valve", "slider"], help="Machine type")
    
    args = parser.parse_args()
    
    print(f"--- Analyzing {args.type.upper()} Recording ---")
    score, raw_mse, visual_b64 = predict(args.file, args.type)
    
    print(f"File: {os.path.basename(args.file)}")
    print(f"Raw Reconstruction Error (MSE): {raw_mse:.6f}")
    print(f"Final Anomaly Score: {score:.4f}")
    
    # Placeholder Logic for Anomaly Decision (Based on your AUC observations)
    # Usually, we set a threshold per machine. For now, let's use a heuristic.
    threshold = -2.5 # This would normally come from your validation set stats
    if score > threshold:
        print("RESULT: 🚨 ANOMALY DETECTED")
    else:
        print("RESULT: ✅ MACHINE HEALTHY")