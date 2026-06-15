import torch
import torch.nn as nn

class PatchEmbed(nn.Module):
    def __init__(self, img_size=(128, 320), patch_size=8, in_chans=1, embed_dim=384):
        super().__init__()
        self.num_patches = (img_size[0] // patch_size) * (img_size[1] // patch_size)
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x):
        x = self.proj(x).flatten(2).transpose(1, 2)
        return x

class ViT(nn.Module):
    def __init__(self, img_size=(128, 320), patch_size=8, embed_dim=384, depth=6, heads=12, latent_dim=256):
        super().__init__()
        self.img_size, self.patch_size = img_size, patch_size
        self.patch_embed = PatchEmbed(img_size, patch_size, 1, embed_dim)
        num_patches = self.patch_embed.num_patches
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches, embed_dim))
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=heads, dim_feedforward=embed_dim*4, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        self.fc_mu = nn.Linear(embed_dim * num_patches, latent_dim)
        self.fc_logvar = nn.Linear(embed_dim * num_patches, latent_dim)
        
        self.decoder_input = nn.Linear(latent_dim, embed_dim * num_patches)
        self.transformer_decoder = nn.TransformerEncoder(encoder_layer, num_layers=depth//2)
        self.recon_head = nn.Linear(embed_dim, patch_size * patch_size)

    def reparameterize(self, mu, logvar):
        return mu + torch.randn_like(mu) * torch.exp(0.5 * logvar)

    def forward(self, x):
        b = x.shape[0]
        x = self.patch_embed(x) + self.pos_embed
        x = self.transformer_encoder(x)
        
        flat = x.reshape(b, -1)
        mu, logvar = self.fc_mu(flat), self.fc_logvar(flat)
        z = self.reparameterize(mu, logvar)
        
        x = self.decoder_input(z).view(b, -1, x.shape[-1])
        x = self.transformer_decoder(x)
        x = self.recon_head(x)
        
        p = self.patch_size
        h, w = self.img_size[0]//p, self.img_size[1]//p
        x = x.reshape(b, h, w, p, p).permute(0, 1, 3, 2, 4).reshape(b, 1, self.img_size[0], self.img_size[1])
        return torch.sigmoid(x), mu, logvar