# Necessary imports for the project.
import torch
import torch.nn as nn
import math

# Defines the input embeddings class
class InputEmbeddings(nn.Module):
    # When we instantiate an input embedding layer we want it to have
    # information about the number of embeddings to create and the dimension
    # that each embedding vector should exist in.
    def __init__(self, d_model: int, vocab_size: int):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model) # nn.Embedding(num_embeddings, embedding_dim)
    
    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)

# Defines the position encoding class
class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, seq_len: int, dropout: float):
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)

        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + (self.pe[:, :x.shape[1], :]).requires_grad(False)
        return self.dropout(x)

class LayerNormalization(nn.Module):

    def __init__(self, eps: float = 10 ** -6):
        super().__init__()
        self.eps = eps
        self.alpha = nn.Parameter(torch.ones[1])
        self.bias = nn.Parameter(torch.zeros[1])
    
    def forward(self, x):
        mean = x.mean(dim = -1, keepdim=True)
        std = x.std(dim = -1, keepdim=True)
        return self.alpha * (x - mean) / (std + self.eps) + self.bias

class FeedForwardBlock(nn.Module):

    def __init__(self, d_model: int, d_ff: int, dropout: float):
        super().__init__()
        self.linear_1 = nn.Linear(d_model, d_ff)
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(d_ff, d_model)
    
    def forward(self, x):
        return self.linear_2(self.dropout(torch.relu(self.linear_1(x))))
    

