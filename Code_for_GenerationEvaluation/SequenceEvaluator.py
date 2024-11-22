class SequenceEvaluator:
    def __init__(self, sequences, action_characterization, evaluation_keys):
        """
        Initializes the SequenceEvaluator.

        :param sequences: List of sequences to evaluate.
        :param action_characterization: Dictionary with action details.
        :param evaluation_keys: List of keys to evaluate.
        """
        self.sequences = sequences
        self.action_characterization = action_characterization
        self.evaluation_keys = evaluation_keys

    @staticmethod
    def evaluate_criterion(criterion_values):
        """
        Evaluates a single criterion across multiple measures in a sequence.

        :param criterion_values: List of criterion values from the sequence.
        :return: The combined evaluation score.
        """
        if all(isinstance(val, str) for val in criterion_values):
            # Combine strings by summing '+' and '-' symbols
            total_pluses = sum(val.count('+') for val in criterion_values)
            total_minuses = sum(val.count('-') for val in criterion_values)
            net_score = total_pluses - total_minuses

            if net_score > 0:
                return '+' * net_score
            elif net_score < 0:
                return '-' * abs(net_score)
            else:
                return '0'

        elif all(isinstance(val, (int, float)) for val in criterion_values):
            # Combine numeric values by summing them
            return sum(criterion_values)

        else:
            raise ValueError("Inconsistent data types in criterion values: must be all strings or all floats/ints.")

    def evaluate_sequence(self, sequence):
        """
        Evaluates a single sequence across all specified evaluation keys.

        :param sequence: A sequence of measures.
        :return: A dictionary of evaluation scores for the sequence.
        """
        evaluation_results = {}

        for key in self.evaluation_keys:
            criterion_values = [
                self.action_characterization[action].get(key, 0)
                for action in sequence
            ]
            evaluation_results[key] = self.evaluate_criterion(criterion_values)

        return evaluation_results

    def evaluate_all_sequences(self):
        """
        Evaluates all sequences and generates the final performance dictionary.

        :return: A dictionary of dictionaries with sequences and their evaluations.
        """
        performance_dict = {}
        for sequence in self.sequences:
            performance_dict[sequence] = self.evaluate_sequence(sequence)
        return performance_dict

