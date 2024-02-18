# saves the openwebtext dataset to a binary file for training. following was helpful:
# https://github.com/HazyResearch/flash-attention/blob/main/training/src/datamodules/language_modeling_hf.py

import os
import glob
from multiprocessing import freeze_support

from tqdm import tqdm
import numpy as np
# import tiktoken
from tokenizers import BertWordPieceTokenizer, Tokenizer
from datasets import load_dataset # huggingface datasets


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
WORKING_DIR = os.path.dirname(DIR_PATH)
IN_DIR = os.path.join(WORKING_DIR, "res01_02")
TOKEN_PATH = os.path.join(WORKING_DIR, "res01_prepare", "tokenizer.json")

data_file = list(glob.glob(IN_DIR + r"\*.txt"))

# number of workers in .map() call
# good number to use is ~order number of cpu cores // 2
num_proc = 4

# we now want to tokenize the dataset. first define the encoding function (gpt2 bpe)

# enc = tiktoken.get_encoding("gpt2")
# enc = SentencePieceBPETokenizer.from_file(
#     vocab_filename=VOCAB_PATH, merges_filename=MERGE_PATH)
enc = Tokenizer.from_file(TOKEN_PATH)

def process(example):
    ids = enc.encode(example['text']).ids
    ids.append(3) # <SEP> 토큰 추가
    # note: I think eot should be prepended not appended... hmm. it's called "eot" though...
    out = {'ids': ids, 'len': len(ids)}
    return out

if __name__ == '__main__':
    print("======== main start ========")
    freeze_support()


    dataset = load_dataset("text", data_files=data_file)

    # owt by default only contains the 'train' split, so create a test split
    split_dataset = dataset["train"].train_test_split(test_size=0.001, seed=1234, shuffle=True)
    split_dataset['val'] = split_dataset.pop('test') # rename the test split to val

    # tokenize the dataset
    tokenized = split_dataset.map(
        process,
        remove_columns=['text'],
        desc="tokenizing the splits",
        num_proc=num_proc,
    )

    print("======== tokenized ========")

    # concatenate all the ids in each dataset into one large file we can use for training
    for split, dset in tokenized.items():
        arr_len = np.sum(dset['len'])
        filename = os.path.join(os.path.dirname(__file__), f'{split}.bin')
        dtype = np.uint16 # (can do since enc.max_token_value == 50256 is < 2**16)
        arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

        print(f"writing {filename}...")
        idx = 0
        for example in tqdm(dset):
            arr[idx : idx + example['len']] = example['ids']
            idx += example['len']
        arr.flush()

    print("======== main end ========")
