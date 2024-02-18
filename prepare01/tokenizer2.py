import os
from collections import defaultdict
from multiprocessing import Pool

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
WORKING_DIR = os.path.dirname(DIR_PATH)
IN_DIR = os.path.join(WORKING_DIR, "res01_01")
OUT_DIR = os.path.join(WORKING_DIR, "res01_02")


processes = 6

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

def writeClean(filepath):
    print(filepath)
    file_name_only = os.path.basename(filepath)
    out_full_path = os.path.join(OUT_DIR, file_name_only)
    out_file = open(out_full_path, encoding='utf8', mode="w")
    new_lines = ""

    in_file = open(filepath, encoding='utf8')
    # split_ch = '⋱'
    for line in in_file:
        new_line = ""
        pos_tags = line.split(" + ")
        for pos_tag in pos_tags:
            word, _ = pos_tag.rsplit("/")
            new_line += (" " + word)
        new_line = new_line.strip()
        new_lines += new_line + "\n"
    out_file.write(new_lines)


def main():
    in_files = readfiles()
    if processes == 1:
        for in_file in in_files:
            writeClean(in_file)
    else:
        pool = Pool(processes=processes)
        pool.map(writeClean, in_files)
    print("==== END ====")



if __name__ == "__main__":
    main()
