import os
import string


class Trie(object):
    def __init__(self):
        self.child = {}

    def insert(self, word, path, line_num, offset):
        current = self.child

        for l in word:
            if l not in current:
                current[l] = {}
                current[l]['/'] = [{"path": path, "line_num": line_num, "offset": offset}]

            elif len(current[l]['/']) <= 5:
                current[l]['/'].append({"path": path, "line_num": line_num, "offset": offset})

            current = current[l]

    def search(self, prefix):
        current = self.child
        curr_prefix = ''

        for l in prefix:
            if l not in current:
                return []

            curr_prefix += l
            current = current[l]

        return current['/']


def edit_sentence(sentence: str):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    return " ".join(sentence.lower().split())


def uploading_files():
    for root, dirs, files in os.walk(f"./data"):
        for file in files:
            curr_path = f"./{root}/{file}"
            with open(curr_path) as file:
                for line_num, line in enumerate(file, 1):
                    yield line, curr_path, line_num


def init_trie(trie):
    for line, path, line_num in uploading_files():
        line = edit_sentence(line)
        offset = 1
        while line != '':
            trie.insert(line, path, line_num, offset)
            line = line[1:]
            offset += 1


def init_data():
    data_trie = Trie()
    init_trie(data_trie)

    return data_trie
