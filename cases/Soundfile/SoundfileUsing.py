# nuitka-project: --standalone
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/test-44100Hz-be-1ch-4bytes.wav=test-44100Hz-be-1ch-4bytes.wav

import os

import soundfile as sf
import numpy as np

rms = [np.sqrt(np.mean(block**2)) for block in
       sf.blocks(os.path.join(os.path.dirname(__file__), 'test-44100Hz-be-1ch-4bytes.wav'), blocksize=1024, overlap=512)]