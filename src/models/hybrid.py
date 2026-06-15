import torch
import torch.nn as nn

class ConvStem(nn.Module):
    """Hybrid Stem: Uses CNN to extract local textures before Transformer."""
    def __init__(self, in_chans=1, embed_dim=384):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv2d(in_chans, embed_dim//4, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(embed_dim//4), nn.GELU(),
            nn.Conv2d(embed_dim//4, embed_dim//2, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(embed_dim//2), nn.GELU(),
            nn.Conv2d(embed_dim//2, embed_dim, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(embed_dim), nn.GELU(),
        )

    def forward(self, x):
        x = self.stem(x) 
        return x.flatten(2).transpose(1, 2) 

class ViT(nn.Module):
    def __init__(self, img_size=(128, 320), embed_dim=384, depth=6, heads=12, latent_dim=256):
        super().__init__()
        self.img_size = img_size
        self.conv_stem = ConvStem(1, embed_dim)
        num_patches = 640 
        
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches, embed_dim))
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=heads, dim_feedforward=embed_dim*4, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        self.fc_mu = nn.Linear(embed_dim * num_patches, latent_dim)
        self.fc_logvar = nn.Linear(embed_dim * num_patches, latent_dim)
        
        self.decoder_input = nn.Linear(latent_dim, embed_dim * num_patches)
        self.transformer_decoder = nn.TransformerEncoder(encoder_layer, num_layers=depth//2)
        
        self.recon_head = nn.Sequential(
            nn.ConvTranspose2d(embed_dim, embed_dim//2, 3, stride=2, padding=1, output_padding=1),
            nn.GELU(),
            nn.ConvTranspose2d(embed_dim//2, embed_dim//4, 3, stride=2, padding=1, output_padding=1),
            nn.GELU(),
            nn.ConvTranspose2d(embed_dim//4, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def reparameterize(self, mu, logvar):
        return mu + torch.randn_like(mu) * torch.exp(0.5 * logvar)

    def forward(self, x):
        b = x.shape[0]
        x = self.conv_stem(x) + self.pos_embed
        x = self.transformer_encoder(x)
        
        flat = x.reshape(b, -1)
        mu, logvar = self.fc_mu(flat), self.fc_logvar(flat)
        z = self.reparameterize(mu, logvar)
        
        x = self.decoder_input(z).view(b, 640, -1).transpose(1, 2).reshape(b, -1, 16, 40)
        x = self.recon_head(x)
        return x, mu, logvar
