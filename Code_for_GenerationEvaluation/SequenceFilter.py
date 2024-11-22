class SequenceFilter:
    def __init__(self, performance_dict, filtering_conditions):
        """
        Initializes the SequenceFilter.

        :param performance_dict: Dictionary of sequences and their performance evaluations.
        :param filtering_conditions: Dictionary specifying filtering conditions for evaluation criteria.
        """
        self.performance_dict = performance_dict
        self.filtering_conditions = filtering_conditions

    @staticmethod
    def compare_criteria(value, condition):
        """
        Compares a single evaluation criterion value against a condition.

        :param value: The value to compare (could be string or float).
        :param condition: The filtering condition tuple (direction, threshold).
        :return: True if the value satisfies the condition, False otherwise.
        """
        direction, threshold = condition

        if isinstance(value, str):
            # Convert the string to a numerical net score for comparison
            value_score = value.count('+') - value.count('-')

            if isinstance(threshold, str):
                threshold_score = threshold.count('+') - threshold.count('-')
            elif isinstance(threshold, list):
                threshold_score = [t.count('+') - t.count('-') for t in threshold]

        elif isinstance(value, (int, float)):
            value_score = value
            if isinstance(threshold, list):
                threshold_score = threshold
            else:
                threshold_score = float(threshold)

        else:
            raise ValueError("Value type not supported for filtering.")

        # Apply filtering logic
        if direction == 'above':
            return value_score > threshold_score
        elif direction == 'below':
            return value_score < threshold_score
        elif direction == 'between':
            return threshold_score[0] <= value_score <= threshold_score[1]
        else:
            raise ValueError(f"Unknown filter direction: {direction}")

    def filter_sequences(self):
        """
        Filters sequences based on the filtering conditions.

        :return: A dictionary of sequences that meet all filtering conditions.
        """
        filtered_performance = {}

        for sequence, evaluations in self.performance_dict.items():
            meets_all_conditions = True

            for criterion, condition in self.filtering_conditions.items():
                if criterion in evaluations:
                    value = evaluations[criterion]
                    if not self.compare_criteria(value, condition):
                        meets_all_conditions = False
                        break

            if meets_all_conditions:
                filtered_performance[sequence] = evaluations

        return filtered_performance