import json
import os


class CorrectionMemory:

    def __init__(self):

        self.memory_file = (
            "learning/memory.json"
        )

        self.rules = self.load()

    def load(self):

        if os.path.exists(
            self.memory_file
        ):

            with open(
                self.memory_file,
                "r"
            ) as f:

                return json.load(f)

        return []

    def save(self):

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                self.rules,
                f,
                indent=4
            )

    def learn(
        self,
        corrections,
        reward
    ):

        for correction in corrections:

            self.rules.append(
                {
                    "error": correction,
                    "reward": reward
                }
            )

        self.save()

    def get_rules(self):

        return self.rules