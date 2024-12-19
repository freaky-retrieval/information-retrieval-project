from parse import *
from PIL import Image, ImageDraw
from utils import get_feature
from sklearn.neighbors import NearestNeighbors 
from dataloader import SimpleImageFolder
from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
import os
sys.path.append(str(Path('tsbir/code/')))
from clip.clip import tokenize, _transform

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
products_list = get_data()
model = get_model().to(device)


sketch_path = 'data/sketches/COCO_val2014_000000163852.jpg'
sketch = Image.open(sketch_path)
caption = 'It is a plate of food.'


image_list = []
for item in os.listdir('data/images'):
    if '.ipynb' not in str(item):
        image_list.append(str(item))


def collate_fn(batch):
    batch = list(filter(lambda x: x is not None, batch))
    return torch.utils.data.dataloader.default_collate(batch)

preprocess_val = _transform(model.visual.input_resolution, is_train=False)
dataset = SimpleImageFolder(image_list, transform=preprocess_val)
dataloader = DataLoader(
    dataset,
    batch_size=32,
    collate_fn=collate_fn,
    shuffle=False,
    num_workers=1,
    pin_memory=True,
    sampler=None,
    drop_last=False,
)


cumulative_loss = 0.0
num_elements = 0.0
all_image_path = []
all_image_features = []
batch_num = 0

with torch.no_grad():
    for batch in dataloader:
        print(f'Batch: {batch_num}', end='')
        images, image_paths = batch
        images = images.to(device, non_blocking=True)

        image_features = model.encode_image(images)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        all_image_features.extend(image_features.cpu().numpy())
        all_image_path.extend(image_paths)

        batch_num += 1
        print(' -- Done\n')
        


query_feat = get_feature(sketch, caption)
feats = all_image_features
nbrs = NearestNeighbors(n_neighbors=10, algorithm='brute', metric='cosine').fit(feats)

def mark_boundary(img, color=(0,255,0)):
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, img.width-5, img.height-5], fill=None, outline=color, width=10)
    return img

def get_image_list(query_feat):

    distances, indices = nbrs.kneighbors(query_feat.cpu().numpy())

    im_list = []
    for ind in indices[0]:
        file_loc = image_paths[ind]
        img = Image.open(file_loc)
        try:
            #if using images from COCO benchmark and sketch from our dataset, we can check id and mark the correct one with green border
            imid = int(sketch_path.split('/')[-1].split('_')[2][:-4])
            cur_imid = int(file_loc.split('/')[-1].split('_')[2].split('.')[0])
            if cur_imid == imid:
                img = mark_boundary(img)
        except:
            img = Image.open(file_loc)
        im_list.append(img)
    return im_list

im_list = [sketch] + get_image_list(query_feat)