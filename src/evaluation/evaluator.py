import torch
import numpy as np
from sklearn.metrics import roc_auc_score

def compute_anomaly_scores(model, dataloader, device):
    model.eval()
    scores = []
    labels = []
    
    with torch.no_grad():
        for data, label in dataloader:
            data = data.to(device)
            recon, mu, logvar = model(data)
            
            # 1. Reconstruction Error (MSE)
            mse = torch.mean(torch.pow(data - recon, 2), dim=(1, 2, 3))
            
            # 2. Latent Regularization Score (KLD per sample)
            kld = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp(), dim=1)
            
            # COMBINED SCORE: MSE is the main signal, KLD catches latent shifts
            final_score = torch.log(mse + 1e-10) + (0.1 * kld)
            
            scores.extend(final_score.cpu().numpy())
            labels.extend(label.numpy())
            
    return np.array(scores), np.array(labels)

def calculate_pauc(y_true, y_score, max_fpr=0.1):
    try:
        return roc_auc_score(y_true, y_score, max_fpr=max_fpr)
    except:
        return 0.5
