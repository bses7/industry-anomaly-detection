
import matplotlib.pyplot as plt
import torch
import numpy as np
from sklearn.metrics import roc_curve, auc
import io
import base64

COL_NORMAL = "#76D7C4"
COL_ABNORMAL = "#F1948A"

def plot_training_results(history, save_path=None):
    """Plots the loss evolution from the training history dictionary."""
    fig, ax = plt.subplots(1, 2, figsize=(16, 5))
    
    ax[0].plot(history['train_loss'], label='Train Loss', color=COL_NORMAL, lw=2)
    ax[0].plot(history['val_loss'], label='Val Loss', color=COL_ABNORMAL, lw=2)
    ax[0].set_title('VAE Total Loss Evolution', fontweight='bold')
    ax[0].set_xlabel('Epochs')
    ax[0].set_ylabel('Loss')
    ax[0].legend()
    
    if 'recon_loss' in history and 'kld_loss' in history:
        ax[1].plot(history['recon_loss'], label='Reconstruction (MSE)', color='#5D6D7E')
        ax[1].plot(history['kld_loss'], label='KL Divergence', color='#F4D03F')
        ax[1].set_title('Reconstruction vs. Latent Regularization', fontweight='bold')
        ax[1].set_xlabel('Epochs')
        ax[1].legend()
    
    plt.tight_layout()
    if save_path: plt.savefig(save_path)
    plt.show()
    plt.close()

def visualize_reconstruction(model, dataloader, device, save_path=None):
    """Takes a sample from the dataloader and shows original vs reconstructed."""
    model.eval()
    with torch.no_grad():
        data, _ = next(iter(dataloader))
        data = data.to(device)
        recon, _, _ = model(data)
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        axes[0].imshow(data[0, 0].cpu().numpy(), aspect='auto', origin='lower', cmap='magma')
        axes[0].set_title("Original Normal Spectrogram", fontweight='bold')
        
        axes[1].imshow(recon[0, 0].cpu().numpy(), aspect='auto', origin='lower', cmap='magma')
        axes[1].set_title("VAE Reconstructed Spectrogram", fontweight='bold')
        
        if save_path: plt.savefig(save_path)
        plt.show()
        plt.close()

def plot_anomaly_results(scores, labels, machine_name, save_path=None):
    """Plots Anomaly Score Distribution and ROC Curve."""
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    normal_scores = scores[labels == 0]
    abnormal_scores = scores[labels == 1]
    
    ax[0].hist(normal_scores, bins=50, alpha=0.6, label='Normal', color="#76D7C4")
    ax[0].hist(abnormal_scores, bins=50, alpha=0.6, label='Abnormal', color="#F1948A")
    ax[0].set_title(f'Anomaly Score Distribution: {machine_name}', fontweight='bold')
    ax[0].set_xlabel('Reconstruction Error (MSE)')
    ax[0].legend()
    
    fpr, tpr, _ = roc_curve(labels, scores)
    roc_auc = auc(fpr, tpr)
    
    ax[1].plot(fpr, tpr, color='#2E4053', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    ax[1].plot([0, 1], [0, 1], color='gray', linestyle='--')
    ax[1].set_xlim([0.0, 1.0])
    ax[1].set_ylim([0.0, 1.05])
    ax[1].set_xlabel('False Positive Rate')
    ax[1].set_ylabel('True Positive Rate')
    ax[1].set_title('Receiver Operating Characteristic (ROC)', fontweight='bold')
    ax[1].legend(loc="lower right")
    
    plt.tight_layout()
    if save_path: plt.savefig(save_path)
    plt.show()
    plt.close()

def get_base64_visual(spec, recon):
    """
    Generates a side-by-side comparison plot and returns it as a Base64 string.
    """
    # Use 'Agg' backend to prevent GUI errors on the server
    plt.switch_backend('Agg')
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Original
    axes[0].imshow(spec[0, 0].cpu().numpy(), aspect='auto', origin='lower', cmap='magma')
    axes[0].set_title("Original Audio Fingerprint")
    axes[0].axis('off')
    
    # Reconstruction
    axes[1].imshow(recon[0, 0].cpu().numpy(), aspect='auto', origin='lower', cmap='magma')
    axes[1].set_title("Model Reconstruction")
    axes[1].axis('off')
    
    plt.tight_layout()
    
    # Save to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    
    # Encode to base64
    return base64.b64encode(buf.getvalue()).decode('utf-8')
