# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import base64
import mimetypes
import os


def data_url_from_file(file_path: str) -> str:
    """Convert a file to a data URL with proper MIME type encoding.

    Args:
      file_path: Path to the file to convert

    Returns:
      Data URL string with format: data:{mime_type};base64,{encoded_content}

    Raises:
      FileNotFoundError: If the file does not exist
      ValueError: If the MIME type cannot be determined
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        raise ValueError(f"Could not determine MIME type of the file: {file_path}")

    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")

    data_url = f"data:{mime_type};base64,{encoded_string}"
    return data_url
