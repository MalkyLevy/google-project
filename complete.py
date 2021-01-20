import linecache
from init import Trie
from init import edit_sentence
from auto_complete_data import AutoCompleteData


def get_sentence_from_path(path: str, line_num: int):
    return linecache.getline(path, line_num)[:-1]


def get_score(sentence_len: int, different_character_index: int = 0, complete_type: str = "simple"):
    score_map = {
        "simple": calculate_score_simple,
        "add": calculate_score_add,
        "delete": calculate_score_delete,
        "replace": calculate_score_replacement
    }

    return score_map[complete_type](sentence_len, different_character_index)


def calculate_score_simple(sentence_len, different_character_index=0):
    return sentence_len * 2


def calculate_score_add(sentence_len, different_character_index):
    minus = 2

    if different_character_index < 4:
        minus = {0: 10, 1: 8, 2: 6, 3: 4}[different_character_index]

    return sentence_len * 2 - minus


def calculate_score_delete(sentence_len, different_character_index):
    minus = 2

    if different_character_index < 4:
        minus = {0: 10, 1: 8, 2: 6, 3: 4}[different_character_index]

    return (sentence_len - 1) * 2 - minus


def calculate_score_replacement(sentence_len, different_character_index):
    minus = 1

    if different_character_index < 4:
        minus = {0: 5, 1: 4, 2: 3, 3: 2}[different_character_index]

    return (sentence_len - 1) * 2 - minus


def replace_char(sentence: str, data_trie: Trie):
    comp_list = []

    for index in range(len(sentence)):
        for char in "abcdefghijklmnopqrstuvwxyz":
            comp_list_of_index = data_trie.search(sentence[:index] + char + sentence[index + 1:])

            for dict_of_index in comp_list_of_index:
                dict_of_index["score"] = get_score(len(sentence), index, "replace")

            comp_list += comp_list_of_index

    return comp_list


def add_char(sentence: str, data_trie: Trie):
    comp_list = []

    for index in range(len(sentence)):
        for char in "abcdefghijklmnopqrstuvwxyz":
            comp_list_of_index = data_trie.search(sentence[:index] + char + sentence[index:])

            for dict_of_index in comp_list_of_index:
                dict_of_index["score"] = get_score(len(sentence), index, "add")

            comp_list += comp_list_of_index

    return comp_list


def delete_char(sentence: str, data_trie: Trie):
    comp_list = []

    for index in range(len(sentence)):
        comp_list_of_index = data_trie.search(sentence[:index] + sentence[index + 1:])

        for dict_of_index in comp_list_of_index:
            dict_of_index["score"] = get_score(len(sentence), index, "delete")

        comp_list += comp_list_of_index

    return comp_list


def search_with_mistake(sentence: str, data_trie: Trie):
    comp_list = []
    comp_list += replace_char(sentence, data_trie)
    comp_list += add_char(sentence, data_trie)
    comp_list += delete_char(sentence, data_trie)

    return comp_list


def sort_res_by_score(auto_complete_list: set):
    best_5_comp = sorted(auto_complete_list, key=lambda obj: obj.get_score_of_obj(), reverse=True)

    return best_5_comp


def search_best_comp(prefix: str, data_trie: Trie):
    edited_prefix = edit_sentence(prefix)
    comp_list = data_trie.search(edited_prefix)
    auto_complete_set = set()

    for comp_dict in comp_list:
        comp_dict["score"] = get_score(len(prefix))

    if len(comp_list) < 5:
        comp_list += search_with_mistake(prefix, data_trie)

    for comp_dict in comp_list:
        sentence = get_sentence_from_path(comp_dict["path"], comp_dict["line_num"])
        auto_comp_obj = AutoCompleteData(sentence, comp_dict["path"], comp_dict["offset"], comp_dict["score"])
        auto_complete_set.add(auto_comp_obj)

    return sort_res_by_score(auto_complete_set)[:5]


def get_best_k_completions(prefix: str, data_trie: Trie):
    comp_list = search_best_comp(prefix, data_trie)

    return comp_list
