# Contributing

Thank you for considering to contribute to `auditus`! Here we provide some general guidelines to streamline the contribution process. The goal of this library is to provide easy access to Audio Embeddings and related transformations. This library is built on [nbdev](https://nbdev.fast.ai/) and therefore requires some familiarity with this library. It also heavily leverages tools from [Answer.AI](https://github.com/AnswerDotAI) like [fasttransform](https://github.com/AnswerDotAI/fasttransform) and [fastcore](https://github.com/AnswerDotAI/fastcore).

## Before you start

- Fork [auditus](https://github.com/CarloLepelaars/auditus) from Github.

- install `auditus` in editable mode:

```bash
pip install -e .
```

## How you can contribute

We always welcome contributions to `auditus`. There are several aspects to this repository:

1. **Transformations:** Audio often requires a series of transformations to get the right array or spectrogram. We welcome contributions of this sort.

2. **Embedding Models:** Besides the HuggingFace Hub, there could be other interesting frameworks for audio embedding models.

## PR submission guidelines

- Keep each PR focused. While it's more convenient, do not combine several unrelated contributions together. It can be a good idea to split contributions into multiple PRs.
- Do not turn an already submitted PR into your development playground. If after you submitted a pull request you discovered that more work is needed - close the PR, do the required work and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
- Make sure to add tests for new features.
