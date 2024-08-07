# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
# SPDX-License-Identifier: Apache-2.0

import pytest

from cv_demos.landmark.hand_landmark_lite_1x1 import run_hand_landmark_lite_1x1
from cv_demos.landmark.palm_detection_lite_1x1 import run_palm_detection_lite_1x1
from cv_demos.landmark.pose_landmark_lite_1x1 import run_pose_landmark_lite_1x1


@pytest.mark.landmark
def test_hand_landmark_lite_1x1(test_device, batch_size):
    run_hand_landmark_lite_1x1(batch_size=batch_size)


@pytest.mark.landmark
def test_palm_detection_lite_1x1(test_device, batch_size):
    run_palm_detection_lite_1x1(batch_size=batch_size)


@pytest.mark.landmark
def test_pose_landmark_lite_1x1(test_device, batch_size):
    run_pose_landmark_lite_1x1(batch_size=batch_size)
