import torch
import torch.nn as nn
import torch.nn.functional as F

class VAE(nn.Module):
    def __init__(self, latent_dim=128):
        super(VAE, self).__init__()
        
        # --- DEEPER ENCODER ---
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 64, 3, stride=2, padding=1),  # [64, 64, 160]
            nn.BatchNorm2d(64), nn.LeakyReLU(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1), # [128, 32, 80]
            nn.BatchNorm2d(128), nn.LeakyReLU(),
            nn.Conv2d(128, 256, 3, stride=2, padding=1), # [256, 16, 40]
            nn.BatchNorm2d(256), nn.LeakyReLU(),
            nn.Conv2d(256, 512, 3, stride=2, padding=1), # [512, 8, 20]
            nn.BatchNorm2d(512), nn.LeakyReLU(),
            nn.Flatten()
        )
        
        # Bottleneck
        self.fc_mu = nn.Linear(512 * 8 * 20, latent_dim)
        self.fc_logvar = nn.Linear(512 * 8 * 20, latent_dim)
        
        # --- DEEPER DECODER ---
        self.decoder_input = nn.Linear(latent_dim, 512 * 8 * 20)
        
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(512, 256, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(256), nn.LeakyReLU(),
            nn.ConvTranspose2d(256, 128, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(128), nn.LeakyReLU(),
            nn.ConvTranspose2d(128, 64, 3, stride=2, padding=1, output_padding=1),
            nn.BatchNorm2d(64), nn.LeakyReLU(),
            nn.ConvTranspose2d(64, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        hidden = self.encoder(x)
        mu = self.fc_mu(hidden)
        logvar = self.fc_logvar(hidden)
        z = self.reparameterize(mu, logvar)
        decoder_input = self.decoder_input(z).view(-1, 512, 8, 20)
        return self.decoder(decoder_input), mu, logvar
