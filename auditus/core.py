"""Audio Embeddings"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['AudioArray', 'load_audio']

# %% ../nbs/00_core.ipynb 3
import numpy as np
from fastcore.all import *
import soundfile as sf
from IPython.display import Audio
from transformers import AutoFeatureExtractor

# %% ../nbs/00_core.ipynb 5
class AudioArray(BasicRepr): 
    def __init__(self, a: np.array, sr: int): store_attr()
    def show(self): return Audio(self, rate=self.sr)
    @property
    def shape(self): return self.a.shape
    def __len__(self): return len(self.a)
    def __getitem__(self, idx): return self.a[idx]

# %% ../nbs/00_core.ipynb 10
def load_audio(path, sr=None): 
    with sf.SoundFile(path) as f: return AudioArray(f.read(), sr if sr else f.samplerate)
