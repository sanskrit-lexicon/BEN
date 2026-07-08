import os
import sys

SANHW1_PATH = "/Users/Shared/sanskrit-lexicon/hwnorm1/sanhw1/sanhw1.txt"

INPUT_HEADER_MAP = {
    "log1.tsv": 3,   # resolution is column 3
    "log2.tsv": 2,   # (not used for primary validation)
}


def load_sanhw1_words(filepath):
    words = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                word = line.split(":")[0]
                words.add(word)
    return words


def in_wordlist(word, wordlist):
    if word in wordlist:
        return True
    # Try without final H (visarga variant)
    if word.endswith("H") and word[:-1] in wordlist:
        return True
    # Try without final m (anusvara variant)
    if word.endswith("m") and word[:-1] in wordlist:
        return True
    # Try without final M (candra-bindu variant)
    if word.endswith("M") and word[:-1] in wordlist:
        return True
    return False


def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = "log1.tsv"

    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = "log3.tsv"

    sanhw1_words = load_sanhw1_words(SANHW1_PATH)
    print(f"Loaded {len(sanhw1_words)} words from sanhw1.txt")

    resolution_col = INPUT_HEADER_MAP.get(os.path.basename(input_path), 3)

    found = 0
    not_found = 0

    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:
        lines = fin.readlines()
        header = lines[0].strip() + "\tin_sanhw1\n"
        fout.write(header)

        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) <= resolution_col:
                continue
            resolution = parts[resolution_col]
            if resolution == "None":
                present = False
            else:
                present = in_wordlist(resolution, sanhw1_words)
            if present:
                found += 1
            else:
                not_found += 1
            fout.write(line + f"\t{present}\n")

    total = found + not_found
    print(f"Found in sanhw1: {found}")
    print(f"Not found in sanhw1: {not_found}")
    print(f"Total: {total}")
    print(f"Written to {output_path}")


if __name__ == "__main__":
    main()
