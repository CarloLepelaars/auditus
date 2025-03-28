# auditus


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

`auditus` gives you simple access to state-of-the-art audio embeddings.
Like [SentenceTransformers](https://sbert.net/) for audio.

``` sh
$ pip install auditus
```

## Quickstart

The high-level object in `auditus` is the
[`AudioPipeline`](https://CarloLepelaars.github.io/auditus/transform.html#audiopipeline)
which takes in a path and returns a pooled embedding.

``` python
from auditus.transform import AudioPipeline

pipe = AudioPipeline(
    # Default AST model
    model_name="MIT/ast-finetuned-audioset-10-10-0.4593", 
    # PyTorch output
    return_tensors="pt", 
    # Resampled to 16KhZ
    target_sr=16000, 
    # Mean pooling to obtain single embedding vector
    pooling="mean",
)

output = pipe("../test_files/XC119042.ogg").squeeze(0)
print(output.shape)
output[:5]
```

    torch.Size([768])

    tensor([0.8653, 1.1659, 0.5956, 0.8498, 0.5322])

To see
[`AudioPipeline`](https://CarloLepelaars.github.io/auditus/transform.html#audiopipeline)
in action on a practical use case, check out [this Kaggle Notebook for
the BirdCLEF+ 2025
competition](https://www.kaggle.com/code/carlolepelaars/generating-audio-embeddings-with-auditus).

## Individual steps

`auditus` offers a range of transforms to process audio for downstream
tasks.

### Loading

Simply load audio with a given sampling rate.

``` python
from auditus.transform import AudioLoader

audio = AudioLoader(sr=32000)("../test_files/XC119042.ogg")
audio
```

    auditus.core.AudioArray(a=array([-2.64216160e-05, -2.54259703e-05,  5.56615578e-06, ...,
           -2.03555092e-01, -2.03390077e-01, -2.45199591e-01]), sr=32000)

The
[`AudioArray`](https://CarloLepelaars.github.io/auditus/core.html#audioarray)
object offers a convenient interface for audio data. For example, you
can listen to the audio in Jupyter Notebooks with `audio.audio()`.

``` python
audio.a[:5], audio.sr, len(audio)
```

    (array([-2.64216160e-05, -2.54259703e-05,  5.56615578e-06, -5.17481631e-08,
            -1.35020821e-06]),
     32000,
     632790)

### Resampling

Many Audio Transformer models work only on a specific sampling rate.
With
[`Resampling`](https://CarloLepelaars.github.io/auditus/transform.html#resampling)
you can resample the audio to the desired sampling rate. Here we go from
32kHz to 16kHz.

``` python
from auditus.transform import Resampling

resampled = Resampling(target_sr=16000)(audio)
resampled
```

    auditus.core.AudioArray(a=array([-2.64216160e-05,  5.56613802e-06, -1.35020873e-06, ...,
           -2.39605007e-01, -2.03555112e-01, -2.45199591e-01]), sr=16000)

### Embedding

The main transform in `auditus` is the
[`AudioEmbedding`](https://CarloLepelaars.github.io/auditus/transform.html#audioembedding)
transform. It takes an
[`AudioArray`](https://CarloLepelaars.github.io/auditus/core.html#audioarray)
and returns a tensor. Check out the [HuggingFace
docs](https://huggingface.co/docs/transformers/model_doc/audio-spectrogram-transformer#transformers.ASTFeatureExtractor)
for more information on the available parameters.

``` python
from auditus.transform import AudioEmbedding

emb = AudioEmbedding(return_tensors="pt")(resampled)
print(emb.shape)
emb[0][:5]
```

    torch.Size([1214, 768])

    tensor([-0.5876,  0.2830, -0.7292,  0.7644, -1.1770])

### Pooling

After generating the embeddings, you often want to pool the embeddings
to a single vector.
[`Pooling`](https://CarloLepelaars.github.io/auditus/transform.html#pooling)
supports `mean` and `max` pooling.

``` python
from auditus.transform import Pooling

pooled = Pooling(pooling="max")(emb)
print(pooled.shape)
pooled[:5]
```

    torch.Size([768])

    tensor([2.8619, 2.7183, 4.1288, 2.6302, 2.2177])
