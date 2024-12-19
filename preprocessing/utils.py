import torch
from PIL import Image
from clip.clip import tokenize, _transform


def generate_image_embedding(model, image_path, transform, device='cuda'):
    """Generate embedding for an image."""
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    
    return embedding.cpu().numpy()

def generate_text_embedding(model, text, device='cuda'):
    """Generate embedding for text."""
    text_token = tokenize([text]).to(device)
    
    with torch.no_grad():
        embedding = model.encode_text(text_token)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    
    return embedding.cpu().numpy()

def get_feature(model, query_sketch, query_text, device='cuda'):

    transformer = _transform(model.visual.input_resolution, is_train=False)
    img1 = transformer(query_sketch).unsqueeze(0).to(device)

    txt = tokenize([str(query_text)])[0].unsqueeze(0).to(device)
    with torch.no_grad():
        sketch_feature = model.encode_sketch(img1)
        text_feature = model.encode_text(txt)
        text_feature = text_feature / text_feature.norm(dim=-1, keepdim=True)
        sketch_feature = sketch_feature / sketch_feature.norm(dim=-1, keepdim=True)

    return model.feature_fuse(sketch_feature,text_feature)


