# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
# SPDX-License-Identifier: Apache-2.0
# VoVNet Model V1

import os
import urllib

import pybuda
import requests
import torch
from PIL import Image
from pybuda._C.backend_api import BackendDevice
from pytorchcv.model_provider import get_model as ptcv_get_model
from torchvision import transforms


def get_image():
    url = "https://raw.githubusercontent.com/pytorch/hub/master/images/dog.jpg"
    input_image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    img_tensor = preprocess(input_image)
    img_tensor = img_tensor.unsqueeze(0)

    return img_tensor


def run_vovnet_v1_39_osmr_pytorch(batch_size=1):

    # Set PyBuda configuration parameters
    compiler_cfg = pybuda.config._get_global_compiler_config()
    compiler_cfg.balancer_policy = "CNN"
    compiler_cfg.default_df_override = pybuda.DataFormat.Float16_b
    compiler_cfg.default_dram_parameters = False

    # Create PyBuda module from PyTorch model
    model = ptcv_get_model("vovnet39", pretrained=True)
    tt_model = pybuda.PyTorchModule("vovnet39_osmr_pt", model)

    # Run inference on Tenstorrent device
    img_tensor = [get_image()] * batch_size
    batch_input = torch.cat(img_tensor, dim=0)
    # Run inference on Tenstorrent device
    output_q = pybuda.run_inference(tt_model, inputs=([batch_input]))
    output = output_q.get()

    # Combine outputs for data parallel runs
    if os.environ.get("PYBUDA_N300_DATA_PARALLEL", "0") == "1":
        concat_tensor = torch.cat((output[0].to_pytorch(), output[1].to_pytorch()), dim=0)
        buda_tensor = pybuda.Tensor.create_from_torch(concat_tensor)
        output = [buda_tensor]

    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    probabilities = torch.nn.functional.softmax(output[0].value(), dim=1)

    # Get ImageNet class mappings
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    image_classes = urllib.request.urlopen(url)
    categories = [s.decode("utf-8").strip() for s in image_classes.readlines()]

    # Show top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    for sample in range(batch_size):
        result = {}  # reset at the start of each new sample
        for i in range(top5_prob.size(1)):
            result[categories[top5_catid[sample][i]]] = top5_prob[sample][i].item()
        print("Sample ID: ", sample, "| Result: ", result)


if __name__ == "__main__":
    run_vovnet_v1_39_osmr_pytorch()
