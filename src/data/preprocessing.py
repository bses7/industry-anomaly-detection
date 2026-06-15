import torch
import torchaudio
import torchaudio.transforms as T
import torch.nn.functional as F
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import librosa

import torch
import torchaudio.transforms as T
import torch.nn.functional as F
import librosa

class AudioTransform:
    def __init__(self, sample_rate=16000, n_mels=128, n_fft=1024, hop_length=512):
        self.mel_spec = T.MelSpectrogram(sample_rate=sample_rate, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
        self.amp_to_db = T.AmplitudeToDB()

    def __call__(self, x):
        spec = self.mel_spec(x)
        spec = self.amp_to_db(spec)
        
        spec = F.pad(spec, (0, 7, 0, 0), mode='constant', value=0)
        
        s_min = spec.min()
        s_max = spec.max()
        spec = (spec - s_min) / (s_max - s_min + 1e-6)
        
        return torch.clamp(spec, 0.0, 1.0)

class MIMIIDataset(Dataset):
    def __init__(self, metadata_df, transform=None, target_sr=16000):
        self.df = metadata_df.reset_index(drop=True)
        self.transform = transform
        self.target_sr = target_sr

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        y, _ = librosa.load(row['path'], sr=self.target_sr)
        waveform = torch.from_numpy(y).unsqueeze(0)
        
        if self.transform:
            spec = self.transform(waveform)
        else:
            spec = waveform
            
        return spec, (1 if row['label'] == 'abnormal' else 0)

def prepare_dataloaders(df, config):
    d_cfg = config['data']
    mask = (df.machine == d_cfg['machine_type'])
    if d_cfg.get('machine_id'): mask &= (df.id == d_cfg['machine_id'])
    if d_cfg.get('snr_level') is not None: mask &= (df.snr.astype(str) == str(d_cfg['snr_level']))
    
    m_df = df[mask]
    norm_df = m_df[m_df.label == 'normal']
    abnorm_df = m_df[m_df.label == 'abnormal']
    
    train_df, val_df = train_test_split(norm_df, test_size=0.15, random_state=42)
    test_df = pd.concat([val_df.sample(frac=0.5, random_state=42), abnorm_df])
    
    tf = AudioTransform(d_cfg['sample_rate'], d_cfg['n_mels'], hop_length=d_cfg['hop_length'])
    
    train_loader = DataLoader(MIMIIDataset(train_df, tf), batch_size=d_cfg['batch_size'], shuffle=True, num_workers=2)
    val_loader = DataLoader(MIMIIDataset(val_df, tf), batch_size=d_cfg['batch_size'], shuffle=False, num_workers=2)
    test_loader = DataLoader(MIMIIDataset(test_df, tf), batch_size=d_cfg['batch_size'], shuffle=False, num_workers=2)
    
    return train_loader, val_loader, test_loader
