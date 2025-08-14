from pydantic import BaseModel, Field


class PeopleMaskParams(BaseModel):
    yolo_confidence_threshold: float = Field(default=0.4, ge=0.0, le=1.0)
    yolo_nms_threshold: float = Field(default=0.9, ge=0.0, le=1.0)


def get_person_masking_workflow_from_params(
    input_url: str, mask_url: str, params: PeopleMaskParams
) -> dict:
    return {
        "input": {
            "workflow": {
                "0": {
                    "inputs": {"url": input_url},
                    "class_type": "Download Image",
                    "_meta": {"title": "Download Image (Gendo)"},
                },
                "1": {
                    "inputs": {
                        "conf_threshold": params.yolo_confidence_threshold,
                        "nms_threshold": params.yolo_nms_threshold,
                        "image": ["0", 0],
                    },
                    "class_type": "YOLOPersonDetectorNode",
                    "_meta": {"title": "YOLO Person Detector"},
                },
                "2": {
                    "inputs": {
                        "sam_model_type": "vit_h",
                        "image": ["0", 0],
                        "bboxes": ["1", 0],
                    },
                    "class_type": "SAMSegmenterNode",
                    "_meta": {"title": "SAM Segmenter (Boxes)"},
                },
                "3": {
                    "inputs": {"mask": ["2", 1]},
                    "class_type": "MaskToImage",
                    "_meta": {"title": "Convert Mask to Image"},
                },
                "4": {
                    "inputs": {"url": mask_url, "images": ["3", 0]},
                    "class_type": "Presigned Upload To S3",
                    "_meta": {"title": "Presigned Upload To S3 (Gendo)"},
                },
            }
        }
    }
