from typing import List, Optional, Callable
from torch_geometric.data import InMemoryDataset, Data
import glob
import os
from pathlib import Path
import torch

class STPyGDataset(InMemoryDataset):
    """
    An in-memory dataset class for handling training using spatial 
    transcriptomics data.
    """
    def __init__(
        self,
        root: str,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        pre_filter: Optional[Callable] = None
    ):
        super().__init__(root, transform, pre_transform, pre_filter)

    @property
    def raw_file_names(self) -> List[str]:
        """
        Return a list of raw file names in the raw directory.

        Returns:
            List[str]: List of raw file names.
        """
        return os.listdir(self.raw_dir)

    @property
    def processed_file_names(self) -> List[str]:
        """
        Return a list of processed file names in the processed directory.

        Returns:
            List[str]: List of processed file names.
        """
        paths = glob.glob(f'{self.processed_dir}/tiles_x=*_y=*_w=*_h=*.pt')
        file_names = list(map(os.path.basename, paths))
        return file_names

    def len(self) -> int:
        """
        Return the number of processed files.

        Returns:
            int: Number of processed files.
        """
        return len(self.processed_file_names)

    def get(self, idx: int) -> Data:
        """
        Get a processed data object.

        Args:
            idx (int): Index of the data object to retrieve.

        Returns:
            Data: The processed data object.
        """
        filepath = Path(self.processed_dir) / self.processed_file_names[idx]
        data = torch.load(filepath)
        data['tx'].x = data['tx'].x.to_dense()
        return data