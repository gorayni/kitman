from kitman.data import DirPathsBuilder, NonZeroBasedIndex


class SequenceIndex:
    def __init__(self, seq_idx, frame_idx):
        self.seq_idx = seq_idx
        self.frame_idx = frame_idx


class SequencePaths(DirPathsBuilder):
    def __init__(self, sequence_path):
        super().__init__(sequence_path, {'frames': ['img1', '{:06d}.jpg'],
                                         'homographies': 'homographies.npy',
                                         'clustered_segmentations': 'clustered_segmentation.npy',
                                         'clustered_means': 'cluster_means_{}.npy',
                                         'clustered_segmentations_bkg': 'clustered_segmentation_bkg_{}.npy',
                                         'clustered_bkg_means': 'cluster_bkg_means_{}.npy',
                                         'segmentations': 'match_gt.npy',
                                         },
                         NonZeroBasedIndex())
        self.sequence = sequence_path
