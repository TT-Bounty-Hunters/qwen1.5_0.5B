# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
# SPDX-License-Identifier: Apache-2.0

import pytest

from audio_demos.whisper.pytorch_whisper_generation import run_whisper_generation

variants = [
    "openai/whisper-tiny",
    "openai/whisper-base",
    "openai/whisper-small",
    "openai/whisper-medium",
    "openai/whisper-large-v2",
]


@pytest.mark.parametrize("variant", variants, ids=variants)
@pytest.mark.whisper
def test_whisper_generation_pytorch(clear_pybuda, test_device, variant, batch_size):
    run_whisper_generation(variant, batch_size=batch_size)
