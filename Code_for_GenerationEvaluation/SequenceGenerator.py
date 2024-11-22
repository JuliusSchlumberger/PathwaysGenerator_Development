import itertools
import random


class SequenceGenerator:
    def __init__(self, action_characterization, N, m):
        """
        Initializes the ActionSequenceGenerator.

        :param action_characterization: Dictionary with action details and interaction rules.
        :param N: Number of sequences to generate.
        :param m: Maximum number of elements in a sequence.
        """
        self.action_characterization = action_characterization
        self.N = N
        self.m = m
        self.actions = list(action_characterization.keys())

    def generate_combinations(self):
        """
        Generates all possible permutations of actions up to the length m.
        """
        possible_combinations = []
        for i in range(1, self.m + 1):
            possible_combinations.extend(itertools.permutations(self.actions, i))
        return possible_combinations

    def is_valid_sequence(self, sequence):
        """
        Validates a sequence based on the requirement rules.

        :param sequence: A tuple representing an action sequence.
        :return: True if the sequence is valid, False otherwise.
        """
        for index, action in enumerate(sequence):
            # Get interaction rules for the current action
            requirements = self.action_characterization[action].get('requirements_action', [])
            for requirement in requirements:
                condition, target = requirement[0], requirement[1]
                if condition == 'blocks':
                    # Target measure cannot follow the current measure
                    if target in sequence[index + 1:]:
                        return False
                elif condition == 'after':
                    # Target measure needs to come before the current measure
                    if target in sequence[index + 1:]:
                        return False
                elif condition == 'before':
                    # Target measure needs to come after the current measure
                    if target not in sequence[index + 1:]:
                        return False
                elif condition == 'directly before':
                    # Target measure needs to come directly after the current measure
                    if target != sequence[index + 1]:
                        return False
                elif condition == 'directly after':
                    # Target measure needs to come directly before the current measure
                    if index == 0 or target != sequence[index - 1]:
                        return False
        return True

    def filter_sequences(self, sequences):
        """
        Filters out invalid sequences based on interaction rules.

        :param sequences: List of action sequences.
        :return: List of valid sequences.
        """
        return [seq for seq in sequences if self.is_valid_sequence(seq)]

    def generate_filtered_sequences(self):
        """
        Generates and filters sequences.

        :return: List of valid sequences.
        """
        # Generate all possible combinations
        possible_combinations = self.generate_combinations()

        # Filter the sequences
        valid_sequences = self.filter_sequences(possible_combinations)

        # Randomly select N sequences
        if len(valid_sequences) > self.N:
            random_combinations = random.sample(valid_sequences, self.N)
        else:
            random_combinations = valid_sequences

        return random_combinations