def check_param(engine_mode, segmentation_mode):
    error_count = 0
    error_list = []

    if not 1 <= engine_mode <= 3:
        # engine mode 0 is legacy mode, which is not supported right now
        error_count += 1
        error_list.append(
            f"engine_mode of {engine_mode} unexpected: value from 1 to including 3 is acceptable. Defaulting to 3."
        )
        engine_mode = 3

    if not 0 <= segmentation_mode <= 11:
        # see "Page segmentation method" on https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html for options
        error_count += 1
        error_list.append(
            f"segmentation_mode of {segmentation_mode} unexpected: value from 0 to including 11 is acceptable. Defaulting to 3."
        )
        segmentation_mode = 3

    config = f"--oem {engine_mode} --psm {segmentation_mode}"

    return error_count, error_list, config
