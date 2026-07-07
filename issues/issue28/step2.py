import re
import sys
from parseheadline import parseheadline


def get_existing_ls(input_file):
    existing = set()
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('<L>'):
                l_part = line.split('<pc>')[0].replace('<L>', '').strip()
                existing.add(l_part)
    return existing


def collect_entries(input_file):
    entries = []
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        if line.startswith('<L>'):
            entry_lines = [line]
            meta = parseheadline(line)
            i += 1
            while i < len(lines):
                el = lines[i].rstrip('\n')
                entry_lines.append(el)
                if el == '<LEND>':
                    break
                i += 1
            entries.append({
                'lines': entry_lines,
                'meta': meta,
                'orig_l': meta['L'] if meta else None,
            })
        else:
            i += 1

    return entries


def process():
    if len(sys.argv) < 3:
        print("Usage: python3 step2.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    print(f"Reading {input_file}...")
    existing_ls = get_existing_ls(input_file)
    print(f"Found {len(existing_ls)} existing L numbers")

    entries = collect_entries(input_file)

    # Identify XYZ entries and assign permanent L numbers
    # Track base -> list of assigned subs
    base_sub_counter = {}

    def next_l_for_base(base_l):
        if base_l not in base_sub_counter:
            existing_subs = set()
            for l in existing_ls:
                if l.startswith(base_l + '.'):
                    try:
                        sub = int(l.split('.')[1])
                        existing_subs.add(sub)
                    except (ValueError, IndexError):
                        pass
            base_sub_counter[base_l] = [2, existing_subs]
            while base_sub_counter[base_l][0] in existing_subs:
                base_sub_counter[base_l][0] += 2
        else:
            base_sub_counter[base_l][0] += 2
            while base_sub_counter[base_l][0] in base_sub_counter[base_l][1]:
                base_sub_counter[base_l][0] += 2
        return f"{base_l}.{base_sub_counter[base_l][0]:03d}"

    # First pass: assign new L numbers to XYZ entries
    # Track first new entry per base for Lbody resolution
    first_new_by_base = {}
    xyz_assignments = {}  # entry index -> new L

    for idx, entry in enumerate(entries):
        orig_l = entry['orig_l']
        if orig_l and '.XYZ' in orig_l:
            base_l = orig_l.replace('.XYZ', '')
            new_l = next_l_for_base(base_l)
            xyz_assignments[idx] = new_l
            if base_l not in first_new_by_base:
                first_new_by_base[base_l] = new_l

    # Write output
    with open(output_file, 'w', encoding='utf-8') as fout, \
         open(log_file, 'w', encoding='utf-8') as flog:
        flog.write("OrigL\tAssignedL\n")

        for idx, entry in enumerate(entries):
            if idx in xyz_assignments:
                new_l = xyz_assignments[idx]
                orig_l = entry['orig_l']
                flog.write(f"{orig_l}\t{new_l}\n")

                for line in entry['lines']:
                    if line.startswith('<L>'):
                        fout.write(line.replace(f"<L>{orig_l}", f"<L>{new_l}") + '\n')
                    elif '{{Lbody=' in line:
                        m = re.search(r'\{\{Lbody=([^}]+)\}\}', line)
                        if m:
                            ref_l = m.group(1)
                            base_ref = ref_l.replace('.XYZ', '')
                            if base_ref in first_new_by_base:
                                line = line.replace(ref_l, first_new_by_base[base_ref])
                        fout.write(line + '\n')
                    else:
                        fout.write(line + '\n')
            else:
                for line in entry['lines']:
                    fout.write(line + '\n')

    print(f"Done. Output: {output_file}, Log: {log_file}")


if __name__ == "__main__":
    process()
