from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
from torch.utils.data.distributed import DistributedSampler
from dataclasses import dataclass
from PIL import Image


@dataclass
class DataInfo:
    dataloader: DataLoader
    sampler: DistributedSampler
    
class SimpleImageFolder(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform
        
    def __getitem__(self, index):
        image_path = self.image_paths[index]
       
        x = Image.open(image_path)
        if self.transform is not None:
            x = self.transform(x)
        return x, image_path
       
        
    
    def __len__(self):
        return len(self.image_paths)