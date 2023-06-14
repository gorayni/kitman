from kitman.data import DirPathsBuilder


class SequenceIndex:
    def __init__(self, seq_idx, frame_idx):
        self.seq_idx = seq_idx
        self.frame_idx = frame_idx


class SequencePaths(DirPathsBuilder):
    def __init__(self, sequence_path):
        super().__init__(sequence_path, {'segmentations': 'match_gt.npy',
                                         'homographies': 'homographies.npy',
                                         'frames': ['img1', '{:06d}.jpg'],
                                         'predicted_segmentations': 'match_predicted.npy',
                                         })
        self.sequence = sequence_path
