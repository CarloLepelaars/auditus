# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_transform.ipynb.

# %% auto 0
__all__ = ['AudioLoader', 'Resampling', 'AudioEmbedding', 'TFAudioEmbedding', 'Pooling', 'AudioPipeline']

# %% ../nbs/01_transform.ipynb 3
import torch
import numpy as np
import soundfile as sf
from fastcore.all import *
import tensorflow as tf

from fasttransform import DisplayedTransform, Pipeline
from transformers import AutoFeatureExtractor

from .core import AudioArray

# %% ../nbs/01_transform.ipynb 7
class AudioLoader(DisplayedTransform):
    """Load audio files into an `AudioArray` object."""
    def __init__(self, sr: int = None): store_attr()
    def encodes(self, x:str) -> AudioArray: return self.load_audio(x, self.sr)

    @staticmethod
    def load_audio(path, sr=None): 
        with sf.SoundFile(path) as f: return AudioArray(f.read(), sr if sr else f.samplerate)

# %% ../nbs/01_transform.ipynb 18
class Resampling(DisplayedTransform):
    """Resample audio to a given sampling rate."""
    def __init__(self, target_sr: int):
        store_attr()
    def encodes(self, audio: AudioArray) -> AudioArray: return self.process_audio_array(audio)
    
    def process_audio_array(self, audio: AudioArray) -> AudioArray:
        if audio.sr == self.target_sr: return audio
        indices = np.linspace(0, len(audio.a) - 1, self._new_length(audio, self.target_sr))
        resampled = np.interp(indices, np.arange(len(audio.a)), audio.a)
        return AudioArray(resampled, self.target_sr)

    def _new_length(self, audio: AudioArray, target_sr: int) -> int:
        return int(len(audio.a) * (target_sr / audio.sr))

# %% ../nbs/01_transform.ipynb 26
class AudioEmbedding(DisplayedTransform):
    """Embed audio using a HuggingFace Audio model."""
    def __init__(self, model_name: str = "MIT/ast-finetuned-audioset-10-10-0.4593", return_tensors: str = "np", **kwargs): 
        store_attr()
        self.model = AutoFeatureExtractor.from_pretrained(model_name, **kwargs)

    def encodes(self, x:AudioArray): return self.call_model(x.a, x.sr)
    
    def call_model(self, x, sr: int):
        return self.model(x, sampling_rate=sr, return_tensors=self.return_tensors)['input_values']

# %% ../nbs/01_transform.ipynb 40
class TFAudioEmbedding(DisplayedTransform):
    """Embed audio using a Tensorflow Hub model."""
    def __init__(self, model_name: str): 
        store_attr()
        self.model = tf.saved_model.load(model_name)

    def encodes(self, x:AudioArray): 
        return self.model.infer_tf(x.a[np.newaxis, :])['embedding'].numpy()

# %% ../nbs/01_transform.ipynb 47
class Pooling(DisplayedTransform):
    """Pool embeddings"""
    def __init__(self, pooling: str):
        assert pooling in [None, "mean", "max"], "Pooling must be either None (no pooling), 'mean' or 'max'."
        store_attr()

    def encodes(self, x:np.ndarray) -> np.ndarray: 
        if self.pooling is None: return x
        elif self.pooling == "mean": return x.mean(axis=1)
        elif self.pooling == "max": return x.max(axis=1)

    def encodes(self, x:torch.Tensor) -> torch.Tensor: 
        if self.pooling is None: return x
        elif self.pooling == "mean": return x.mean(dim=1)
        elif self.pooling == "max": return x.max(dim=1)[0]

# %% ../nbs/01_transform.ipynb 64
class AudioPipeline(Pipeline):
    def __init__(self, 
                 model_name: str = "MIT/ast-finetuned-audioset-10-10-0.4593", 
                 return_tensors: str = "np",
                 target_sr: int = 16_000, 
                 pooling: str = "max", 
                 **kwargs):
        super().__init__([
            AudioLoader(),
            Resampling(target_sr),
            AudioEmbedding(model_name, return_tensors, **kwargs),
            Pooling(pooling)
        ])
