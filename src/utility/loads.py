
def load_word_dict(file, delimiter):
    body = file.read_text().split("\n")
    body = [b for b in body if b and not b.startswith("#")]
    body = [b.split(delimiter) for b in body]
    body = [[wrd.strip(), [phn.strip() for phn in phns.split(" ") if phn]] for wrd, phns in body]
    return {wrd: phns for wrd, phns in body}

def load_sentences(file, repeat=1):
    body = file.read_text().split("\n")
    body = [b for b in body if b and not b.startswith("#")]
    body = [b.split(":")[-1].strip() for b in body]
    return [[wrd.strip() for wrd in snt.split(" ") if wrd] for snt in body if snt]

def load_stems(file, repeat=1):
    body = file.read_text().split("\n")
    body = [b for b in body if b and not b.startswith("#")]
    body = [b.split(":")[0].strip().replace(" ", "_") for b in body]
    return body
