from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
from torch.utils.data.distributed import DistributedSampler
from dataclasses import dataclass
from PIL import Image


@dataclass
class DataInfo:
    dataloader: DataLoader
    sampler: DistributedSampler
    
class SimpleImageFolder(Dataset):
    def __init__(self, image_paths):
        self.image_paths = image_paths
        
    def __getitem__(self, index):
        image_path = self.image_paths[index]
       
        return image_path
       
        
    
    def __len__(self):
        return len(self.image_paths)