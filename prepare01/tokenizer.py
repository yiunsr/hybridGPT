import os
import re
from kiwipiepy import Kiwi
from multiprocessing import Pool

# from kss import split_sentences
kiwi = Kiwi()

processes = 6

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
WORKING_DIR = os.path.dirname(DIR_PATH)
IN_DIR = os.path.join(WORKING_DIR, "res_raw")
OUT_DIR = os.path.join(WORKING_DIR, "res01_01")

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

def getHangulType(text):
    idx = 0
    meta = dict(hasBracket=False)
    length = len(text)
    inBracket = False
    for idx in range(length):
        char = text[idx]
        if inBracket and char == ")":
            inBracket = False
            idx += 1
            continue
        elif char == "(":
            inBracket = True
            idx += 1
            meta["hasBracket"] = True
        elif '가' <= char <= '힣':
            idx += 1
            continue
        elif 'ㄱ' <= char <= 'ㆎ':
            idx += 1
            continue
        elif char in (" ", ".", ".", "!", "?",  "~", "\n",):
            idx += 1
            continue
        elif char in ("『", "』"):
            idx += 1
            continue
        # elif char in ("“", "”","‘", "’", "⋯",):
        #     idx += 1
        #     continue
        elif "A" <= char <= "Z":
            idx += 1
            continue
        elif "0" <= char <= "9":
            idx += 1
            continue
        # elif char in "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳":
        #     idx += 1
        #     continue
        return False, meta
    return True, meta

def split_sentences(line):
    re_end = r"([다|나|오|요|까|어|건|대|랑|만][.|?|!]+)"
    matchItems = re.finditer(re_end, line)
    sens = []
    lastIndex = 0
    for matchItem in matchItems:
        sen = line[lastIndex:matchItem.regs[0][1]]
        lastIndex = matchItem.regs[0][1]
        sen = sen.strip()
        sens.append(sen)
    return sens


HAN_START = ord('가')
CHO = ('ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 
    'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')
JUNG = ('ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ')
# JONG = ('', 'ᆨ', 'ᆩ', 'ᆪ', 'ᆫ', 'ᆬ', 'ᆭ', 'ᆮ', 'ᆯ', 'ᆰ', 
#     'ᆱ', 'ᆲ', 'ᆳ','ᆴ', 'ᆵ', 'ᆶ', 'ᆷ', 'ᆸ', 'ᆹ', 'ᆺ', 
#     'ᆻ', 'ᆼ', 'ᆽ', 'ᆾ', 'ᆿ', 'ᇀ', 'ᇁ', 'ᇂ')
JONG = ('', 'ﾡ', 'ﾢ', 'ﾣ', 'ﾤ', 'ﾥ', 'ﾦ', 'ﾧ', 'ﾩ','ﾪ', 
    'ﾫ', 'ﾬ', 'ﾭ','ﾮ', 'ﾯ', 'ﾰ', 'ﾱ', 'ﾲ', 'ﾴ', 'ﾵ',
    'ﾶ', 'ﾷ', 'ﾸ', 'ﾺ', 'ﾻ', 'ﾼ', 'ﾽ', 'ﾾ')

def sen2jamo(sen):
    new_sen = ""
    
    for char in sen:
        if char < '가' or char > '힣':
            new_sen += char
            continue
        relative_pos = ord(char) - HAN_START
        cho = int( relative_pos / (21 * 28) )
        jung = int( (relative_pos - cho * 21 * 28) / 28)
        jong = relative_pos - cho * 21 * 28 - jung * 28
        first = cho * (21 * 28) + jung * 28 + HAN_START
        new_sen += (chr(first) + JONG[jong])
    return new_sen

def koTokenizer(sen):
    # return sen2jamo(sen)
    postags = kiwi.tokenize(sen)
    new_postag = []
    for postag in postags:
        new_postag.append(postag.tagged_form)
        # for idx, (word, tag) in enumerate(postag):
        #     word = sen2jamo(word)
        #     if idx == 0:
        #         new_eojeol = word
        #     elif tag.startswith("J"):
        #         new_eojeol += split_ch + word
        #     elif tag.startswith("S"):  
        #         # SE 마침표, 물음표, 느낌표
        #         new_eojeol += word
        #     else:
        #         new_eojeol += split_ch + word
        # newWords.append(new_eojeol)
    new_sen = " + ".join(new_postag)
    return new_sen

pattern = r'\([^)]*\)'

    
def tokenFile(file_path):
    file_name_only = os.path.basename(file_path)
    print(file_name_only)
    in_file = open(file_path, encoding='utf8')
    out_full_path = os.path.join(OUT_DIR, file_name_only)
    out_file = open(out_full_path, encoding='utf8', mode="w")
    new_lines = ""
    line_index = 0
    for line in in_file:
        line = line.strip()
        if len(line) < 25:
            continue
        line = re.sub(pattern=pattern, repl='', string= line)
        if len(line) < 25:
            continue

        sens = split_sentences(line)
        new_line = ""
        sen_index = 0
        for sen in sens:
            isHangulOnly, meta = getHangulType(sen)
            if isHangulOnly is False: 
                if sen_index > 1:
                    new_line = koTokenizer(new_line)
                    new_lines += new_line + "\n"
                    line_index += 1
                new_line = ""
                sen_index = 0
                continue

            sen_index += 1
            new_line += sen

            if len(new_line) > 300 and sen_index > 1:
                new_line = koTokenizer(new_line)
                new_lines += new_line + "\n"
                new_line = ""
                sen_index = 0
                line_index += 1
        
        # if line_index > 500:
        #     break
    out_file.write(new_lines)

def main():
    in_files = readfiles()
    if processes == 1:
        for in_file in in_files:
            tokenFile(in_file)
    else:
        pool = Pool(processes=6)
        pool.map(tokenFile, in_files)

    # for file_path in in_files:
    #     tokenFile(file_path)

if __name__ == "__main__":
    main()
