import re
import sys
import os
from parseheadline import parseheadline
from slp1 import iast_to_slp1, slp1_to_iast

def adjust_hw_prefix(prefix_slp1, base_slp1, lid, manually_mapped=None):
    result = _adjust_hw_prefix_internal(prefix_slp1, base_slp1)
    if result is None and manually_mapped is not None:
        key = (lid, base_slp1, prefix_slp1)
        if key in manually_mapped:
            return manually_mapped[key]
    return result


def _adjust_hw_prefix_internal(prefix, base):
    pref = prefix.rstrip('-')
    if not pref:
        return base

    # Base starts with vowel
    vowels = set('aiuUfFeEoOA')
    if base and base[0] in vowels:
        # Prefix ends with a/A
        if pref and pref[-1] in 'aA':
            if base[0] in 'aA':
                return pref[:-1] + 'A' + base[1:]
            elif base[0] in 'iI':
                return pref[:-1] + 'e' + base[1:]
            elif base[0] in 'uU':
                return pref[:-1] + 'o' + base[1:]
            elif base[0] in 'fF':
                return pref[:-1] + 'ar' + base[1:]
            elif base[0] == 'e':
                return pref[:-1] + 'ai' + base[1:]
            elif base[0] == 'o':
                return pref[:-1] + 'au' + base[1:]
            elif base[0] == 'E':
                return pref[:-1] + 'A' + base[1:]
            elif base[0] == 'O':
                return pref[:-1] + 'A' + base[1:]
        # Prefix ends with i/I
        elif pref and pref[-1] in 'iI':
            return pref[:-1] + 'y' + base
        # Prefix ends with u/U
        elif pref and pref[-1] in 'uU':
            return pref[:-1] + 'v' + base
        # Prefix ends with f/F
        elif pref and pref[-1] in 'fF':
            return pref[:-1] + 'r' + base
        # Prefix ends with e
        elif pref and pref[-1] == 'e':
            return pref[:-1] + 'ay' + base
        # Prefix ends with o
        elif pref and pref[-1] == 'o':
            return pref[:-1] + 'av' + base
        # Prefix ends with consonant
        else:
            return pref + base
    else:
        # Base starts with consonant
        # Handle visarga sandhi
        if pref and pref[-1] == 'H':
            # H + k/K/p/P -> corresponding sibilant + k/K/p/P
            if base[0] in 'kKpP':
                sibilant = {'k': 'k', 'K': 'k', 'p': 'p', 'P': 'p'}
                return pref[:-1] + 'S' + base if base[0] in 'kK' else pref[:-1] + 's' + base
            # H + sibilant/c/t/T -> sibilant stays, H disappears
            elif base[0] in 'SsCwWqQz':
                return pref[:-1] + base
            # H + other consonant -> r + consonant
            else:
                return pref[:-1] + 'r' + base
        else:
            return pref + base

    return None


def extract_compound_info(line):
    m = re.search(r'{%([^}]+)%}', line)
    if not m:
        return None, None, line
    content = m.group(1)
    rest = line[m.end():]
    return content, rest, line


def process_entry(metaline, lines, fout, flog, correct, wrong, manually_mapped):
    meta = parseheadline(metaline)
    lid = meta['L']
    basehw = meta['k1']

    # Find the prefix (text before first ¦) for building new entry definitions
    pref = ''
    for l in lines:
        if '¦' in l:
            pref = l.split('¦')[0].strip()
            break

    # Find --<ab>Comp.</ab> section
    comp_idx = None
    for i, line in enumerate(lines):
        if '--<ab>Comp.</ab>' in line:
            comp_idx = i
            break

    if comp_idx is None:
        for line in lines:
            fout.write(line + '\n')
        return correct, wrong

    # Collect all lines after Comp. until next --<ab> or <LEND>
    # Separate those that are compound lines (starting with ¦) from body text
    compound_lines = []
    body_after_comp = []
    after_comp = False
    in_comp_section = False
    for i, line in enumerate(lines):
        if i == comp_idx:
            after_comp = True
            in_comp_section = True
            continue
        if after_comp:
            stripped = line.strip()
            if line == '<LEND>':
                break
            if stripped.startswith('--<ab>') and 'Comp' not in stripped:
                in_comp_section = False
                body_after_comp.append(line)
                continue
            if in_comp_section:
                if stripped.startswith('¦'):
                    compound_lines.append(line)
                else:
                    body_after_comp.append(line)
            else:
                body_after_comp.append(line)

    if not compound_lines:
        for line in lines:
            fout.write(line + '\n')
        return correct, wrong

    # Write parent entry: everything before and including --<ab>Comp.</ab> + body_after_comp + <LEND>
    parent_content = lines[:comp_idx + 1] + body_after_comp + ['<LEND>']
    for line in parent_content:
        fout.write(line + '\n')

    # Process each compound line
    new_entries_data = []
    for cl in compound_lines:
        m = re.search(r'{%([^}]+)%}', cl)
        if not m:
            continue
        compound_content = m.group(1)
        rest_of_line = cl[m.end():]

        is_prefix = compound_content.endswith('-')
        if is_prefix:
            prefix_stem = compound_content.rstrip('-')
            prefix_slp1 = iast_to_slp1(prefix_stem)
            suggestion = adjust_hw_prefix(prefix_slp1, basehw, lid, manually_mapped)
            if suggestion:
                correct[0] += 1
                flog.write(f'{lid}\t{basehw}\t{compound_content}\t{suggestion}\n')
            else:
                wrong[0] += 1
                flog.write(f'{lid}\t{basehw}\t{compound_content}\tNone\n')
            new_headword = suggestion
        else:
            suggestion = iast_to_slp1(compound_content)
            correct[0] += 1
            flog.write(f'{lid}\t{basehw}\t{compound_content}\t{suggestion}\n')
            new_headword = suggestion

        # Build body line: {#prefix_slp1#} + {#base_slp1#}¦ {%prefix_iast%} + {%base_iast%}, rest
        base_iast = slp1_to_iast(basehw)
        if is_prefix:
            prefix_body_slp1 = f"{{#{prefix_slp1}-#}}"
            prefix_body_iast = f"{{%{compound_content}%}}"
        else:
            prefix_body_slp1 = f"{{#{iast_to_slp1(compound_content)}#}}"
            prefix_body_iast = f"{{%{compound_content}%}}"
        base_body_slp1 = f"{{#{basehw}#}}"
        base_body_iast = f"{{%{base_iast}%}}"
        new_body = f"{prefix_body_slp1} + {base_body_slp1}¦ {prefix_body_iast} + {base_body_iast}{rest_of_line}"

        k2_value = f"{prefix_slp1}-{basehw}" if is_prefix else new_headword

        entry_data = {
            'new_headword': new_headword,
            'k2_value': k2_value,
            'body_line': new_body,
        }
        new_entries_data.append(entry_data)

    # Write new derived entries
    for sidx, ed in enumerate(new_entries_data):
        fout.write('\n')
        suggestion = ed['new_headword']
        if suggestion:
            metaline1 = metaline.replace('<k1>' + basehw, '<k1>' + suggestion)
            metaline1 = metaline1.replace('<k2>' + basehw, '<k2>' + ed['k2_value'])
            metaline1 = metaline1.replace('<pc>', '.XYZ<pc>')
        else:
            metaline1 = metaline.replace('<k2>', '.ABC<k2>')
            metaline1 = metaline1.replace('<e>', '.ABC<e>')
            metaline1 = metaline1.replace('<pc>', '.XYZ<pc>')

        fout.write(metaline1 + '\n')
        fout.write(ed['body_line'] + '\n')

        fout.write('<LEND>\n')

    return correct, wrong


def load_manually_mapped(filepath):
    mapping = {}
    if not filepath or not os.path.exists(filepath):
        return mapping
    with open(filepath, 'r', encoding='utf-8') as f:
        f.readline()
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split('\t')
            if len(parts) < 4: continue
            key = (parts[0], parts[1], parts[2])
            mapping[key] = parts[3]
    return mapping


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 step1.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    manually_mapped = load_manually_mapped("manually_mapped.tsv")
    print(f"Loaded {len(manually_mapped)} manual mappings")

    fout = open(output_file, 'w', encoding='utf-8')
    flog = open(log_file, 'w', encoding='utf-8')
    flog.write('Lnum\tbasehw\tcompound\tresolution\n')
    correct = [0]
    wrong = [0]

    with open(input_file, 'r', encoding='utf-8') as fin:
        entry_lines = []
        metaline = None

        for lin in fin:
            lin = lin.rstrip('\n')

            if lin.startswith('<L>'):
                if metaline and entry_lines:
                    process_entry(metaline, entry_lines, fout, flog, correct, wrong, manually_mapped)
                metaline = lin
                entry_lines = []
                fout.write(lin + '\n')

            elif lin == '<LEND>':
                entry_lines.append(lin)
                process_entry(metaline, entry_lines, fout, flog, correct, wrong, manually_mapped)
                entry_lines = []
                metaline = None

            else:
                if metaline is not None:
                    entry_lines.append(lin)
                else:
                    fout.write(lin + '\n')

        if metaline and entry_lines:
            process_entry(metaline, entry_lines, fout, flog, correct, wrong, manually_mapped)

    total = correct[0] + wrong[0]
    print(f'Resolved: {correct[0]}, Unresolved: {wrong[0]}, Total: {total}')
    fout.close()
    flog.close()
