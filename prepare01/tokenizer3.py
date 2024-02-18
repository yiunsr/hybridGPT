import os
from tokenizers import BertWordPieceTokenizer


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
WORKING_DIR = os.path.dirname(DIR_PATH)
IN_DIR = os.path.join(WORKING_DIR, "res01_02")
OUT_DIR = os.path.join(WORKING_DIR, "res01_prepare")

def readfiles():
    out_filenames = []
    for file in os.listdir(OUT_DIR):
        out_filenames.append(file)

    in_files = []
    for file in os.listdir(IN_DIR):
        # 이미 OUT_DIR 있는 파일은 작업이 끝나서 continue
        if file in out_filenames:
            continue
        full_path = os.path.join(IN_DIR, file)
        in_files.append(full_path)
    return in_files


def main():
    in_files = readfiles()
    tokenizer = BertWordPieceTokenizer(
        strip_accents=False,
        lowercase=False)
    st = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", 
        "[TITLE]",
        "[UNK]", "[UNK0]", "[UNK1]",
        "[UNK3]", "[UNK4]", "[UNK5]", "[UNK6]", "[UNK7]", "[UNK9]", "[UNK9]"]
    tokenizer.train(files=in_files, 
        vocab_size=12288, min_frequency=5,
        special_tokens = st,)
    tokenizer.save_model(OUT_DIR)
    tokenizer.save(OUT_DIR + "/tokenizer.json")


if __name__ == "__main__":
    main()
