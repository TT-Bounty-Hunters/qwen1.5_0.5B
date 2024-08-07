# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
# SPDX-License-Identifier: Apache-2.0

# DPR Demo Script - Reader

import pybuda
from transformers import DPRReader, DPRReaderTokenizer


def run_dpr_reader_pytorch(variant="facebook/dpr-reader-multiset-base", batch_size=1):

    # Load Bert tokenizer and model from HuggingFace
    # Variants: facebook/dpr-reader-single-nq-base, facebook/dpr-reader-multiset-base
    model_ckpt = variant
    tokenizer = DPRReaderTokenizer.from_pretrained(model_ckpt)
    model = DPRReader.from_pretrained(model_ckpt)

    compiler_cfg = pybuda.config._get_global_compiler_config()  # load global compiler config object
    compiler_cfg.default_df_override = pybuda._C.DataFormat.Float16_b

    # Data preprocessing
    input_tokens = tokenizer(
        questions=["What is love?"] * batch_size,
        titles=["Haddaway"] * batch_size,
        texts=["'What Is Love' is a song recorded by the artist Haddaway"] * batch_size,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )

    # Run inference on Tenstorrent device
    output_q = pybuda.run_inference(
        pybuda.PyTorchModule("pt_dpr_reader", model),
        inputs=[input_tokens],
    )
    output = output_q.get()

    # Postprocessing
    start_logits = output[0].value()
    end_logits = output[1].value()
    relevance_logits = output[2].value()

    # Print Outputs
    for sample_id in range(batch_size):
        print(
            f"Sample ID: {sample_id} | Start Logits: {start_logits[sample_id]} | End Logits: {end_logits[sample_id]} | Relevance Logits: {relevance_logits[sample_id]}"
        )


if __name__ == "__main__":
    run_dpr_reader_pytorch()
