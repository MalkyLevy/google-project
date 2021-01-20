from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    def __init__(self, sentence: str, source: str, offset: int, score: int):
        self.completed_sentence = sentence
        self.source_text = source
        self.offset = offset
        self.score = score

    def __hash__(self):
        return hash((self.completed_sentence, self.source_text, self.offset, self.score))

    def auto_comp_print(self):
        print(self.completed_sentence, f"(score: {self.score})")

    def get_score_of_obj(self):
        return self.score

    def get_sentence(self):
        return self.completed_sentence
