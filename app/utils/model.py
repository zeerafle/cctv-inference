from transformers import DetrImageProcessor, DetrForObjectDetection


def load_model():
    processor = DetrImageProcessor.from_pretrained('facebook/detr-resnet-50')
    model = DetrForObjectDetection.from_pretrained("hilmantm/detr-traffic-accident-detection")
    return processor, model
