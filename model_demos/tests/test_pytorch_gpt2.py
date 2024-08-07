# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
# SPDX-License-Identifier: Apache-2.0

import pytest

from nlp_demos.gpt2.gpt2_text_generation import run_gpt2_text_gen


@pytest.mark.gpt2
def test_gpt2_pytorch(clear_pybuda, test_device, batch_size):
    run_gpt2_text_gen(batch_size=batch_size)
