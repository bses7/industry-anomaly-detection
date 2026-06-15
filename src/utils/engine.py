import torch
import torch.nn.functional as F
from tqdm import tqdm

def train_vae(model, train_loader, val_loader, optimizer, config, device):
    history = {'train_loss': [], 'val_loss': [], 'recon_loss': [], 'kld_loss': []}
    epochs = config['train']['epochs']
    patience = config['train']['early_stopping_patience']
    
    BETA = 1.0 
    best_loss = float('inf')
    counter = 0 
    
    for epoch in range(epochs):
        model.train()
        t_loss, t_recon, t_kld = 0, 0, 0
        
        for data, _ in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
            data = data.to(device)
            optimizer.zero_grad()
            recon, mu, logvar = model(data)
            
            recon_loss = F.mse_loss(recon, data, reduction='mean')
            
            kld_loss = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
            
            loss = recon_loss + (BETA * kld_loss)
            
            loss.backward()
            
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            t_loss += loss.item()
            t_recon += recon_loss.item()
            t_kld += kld_loss.item()

        model.eval()
        v_loss = 0
        with torch.no_grad():
            for data, _ in val_loader:
                data = data.to(device)
                recon, mu, logvar = model(data)
                v_recon = F.mse_loss(recon, data, reduction='mean')
                v_kld = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
                v_loss += (v_recon + (BETA * v_kld)).item()
        
        n_batches = len(train_loader)
        history['train_loss'].append(t_loss / n_batches)
        history['recon_loss'].append(t_recon / n_batches)
        history['kld_loss'].append(t_kld / n_batches)
        history['val_loss'].append(v_loss / len(val_loader))
        
        avg_val_loss = history['val_loss'][-1]
        print(f"Epoch {epoch+1} | Loss: {history['train_loss'][-1]:.6f} | Val Loss: {avg_val_loss:.6f}")
        
        if avg_val_loss < best_loss:
            best_loss = avg_val_loss
            torch.save(model.state_dict(), config['train']['save_path'])
            counter = 0
            print("⭐ New best model saved!")
        else:
            counter += 1
            if counter >= patience: 
                print(f"🛑 Early stopping triggered after {epoch+1} epochs.")
                break
            
    return history
