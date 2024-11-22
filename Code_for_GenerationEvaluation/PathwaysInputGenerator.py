import numpy as np

class PathwaysInputGenerator:
    def __init__(self, filtered_sequences, action_characterization, scenario=None):
        """
        Initializes the PathwaysInputGenerator.

        :param filtered_sequences: List of filtered sequences of actions.
        :param action_characterization: Dictionary with action details.
        :param scenario: Optional dictionary with time-series information.
        """
        self.filtered_sequences = filtered_sequences
        self.action_characterization = action_characterization
        self.scenario = scenario

    @staticmethod
    def aggregate_effectiveness(sequence, action_characterization, up_to_index):
        """
        Aggregates effectiveness values for the actions in a sequence up to the given index.

        :param sequence: The sequence of actions.
        :param action_characterization: Dictionary with action details.
        :param up_to_index: The index up to which effectiveness is aggregated.
        :return: The aggregated effectiveness as a string or float.
        """
        aggregated_value = 0
        for i in range(up_to_index + 1):
            value = action_characterization[sequence[i]]['effectiveness']
            if isinstance(value, str):
                plus_count = value.count('+')
                minus_count = value.count('-')
                aggregated_value += plus_count - minus_count
            elif isinstance(value, (int, float)):
                aggregated_value += value

        if isinstance(aggregated_value, int) and aggregated_value > 0 and isinstance(value, str):
            return '+' * aggregated_value
        elif isinstance(aggregated_value, int) and aggregated_value < 0 and isinstance(value, str):
            return '-' * abs(aggregated_value)
        elif isinstance(aggregated_value, int) and isinstance(value, str):
            return '0'
        return aggregated_value

    @staticmethod
    def interpolate_time(effectiveness_value, scenario):
        """
        Interpolates the time for a given effectiveness value based on the scenario time-series.

        :param effectiveness_value: The effectiveness value to find in the scenario.
        :param scenario: The scenario time-series data.
        :return: Interpolated time for the effectiveness value.
        """
        effectiveness_values = np.array(list(scenario.values()))
        times = np.array(list(scenario.keys()))

        if effectiveness_value in effectiveness_values:
            return scenario[effectiveness_value]
        else:
            idx = np.searchsorted(effectiveness_values, effectiveness_value)
            if idx == 0 or idx == len(effectiveness_values):
                raise ValueError(
                    f"The timeseries is too short. It only captrues the range from year {times[0]} "
                    f"({effectiveness_values[0]}) to {times[len(effectiveness_values)]} "
                    f"({effectiveness_values[len(effectiveness_values)]}), not including {effectiveness_value}.")  # Out of range
            lower_eff, upper_eff = effectiveness_values[idx - 1], effectiveness_values[idx]
            lower_time, upper_time = times[idx - 1], times[idx]
            # Linear interpolation
            interpolated_time = lower_time + (upper_time - lower_time) * (
                (effectiveness_value - lower_eff) / (upper_eff - lower_eff)
            )
            return interpolated_time

    def generate_instance_dict(self):
        """
        Generates the input files for the Pathways Generator.

        :return: A dictionary of dictionaries structured for input files.
        """
        self.instance_dict = {}

        for sequence in self.filtered_sequences:
            for idx, action in enumerate(sequence):
                precondition = sequence[:idx]  # All elements up to (excluding) the current element
                if action not in self.instance_dict:
                    self.instance_dict[action] = {}
                if precondition not in self.instance_dict[action]:
                    self.instance_dict[action][precondition] = {}

                # Calculate xposition
                if self.scenario:
                    effectiveness_value = self.aggregate_effectiveness(sequence, self.action_characterization, idx)
                    xposition = self.interpolate_time(effectiveness_value, self.scenario)
                else:
                    xposition = self.aggregate_effectiveness(sequence, self.action_characterization, idx)

                self.instance_dict[action][precondition]['xposition'] = xposition

    @staticmethod
    def translate_effectiveness_to_int(effectiveness_value):
        """
        Translates effectiveness strings ('+', '-', '0') into integers.

        :param effectiveness_value: The effectiveness value as a string or numeric.
        :return: Translated integer value.
        """
        if isinstance(effectiveness_value, str):
            plus_count = effectiveness_value.count('+')
            minus_count = effectiveness_value.count('-')
            return plus_count - minus_count
        return effectiveness_value

    def create_xpositions_file(self, end_current_system, output_file='xpositions.txt'):
        """
        Creates the xpositions.txt file from the input dictionary.

        :param end_current_system: tipping point of current system. Default: 0
        :param output_file: The name of the output file.
        """
        xpositions_list = [('current', end_current_system)]

        for action, precondition_dict in self.instance_dict.items():
            action_key = action.replace(' ', '')  # Remove whitespaces
            for idx, (precondition, data) in enumerate(precondition_dict.items()):
                xposition_value = data.get('xposition', 0)
                # Translate effectiveness to int if it's a string
                xposition_value = self.translate_effectiveness_to_int(xposition_value) + end_current_system
                xpositions_list.append((f"{action_key}[{idx}]", xposition_value))

        # Write the file
        with open(output_file, 'w') as file:
            for key, value in xpositions_list:
                file.write(f"{key} {value}\n")

        print(f"File '{output_file}' created successfully.")

    def create_sequences_file(self, output_file='sequences.txt'):
        """
        Creates the sequences.txt file from the input dictionary and filtered sequences.

        :param output_file: The name of the output file.
        """
        sequences_list = []

        for sequence in self.filtered_sequences:
            for i in range(len(sequence) - 1):
                first_action = sequence[i]
                second_action = sequence[i + 1]

                # Identify preconditions and their indices for both actions
                first_precondition = sequence[:i]
                second_precondition = sequence[:i + 1]

                first_idx = list(self.instance_dict[first_action].keys()).index(first_precondition)
                second_idx = list(self.instance_dict[second_action].keys()).index(second_precondition)

                first_key = f"{first_action.replace(' ', '')}[{first_idx}]"
                second_key = f"{second_action.replace(' ', '')}[{second_idx}]"

                if i == 0:
                    # Add the 'current' line for the first action in the sequence
                    sequences_list.append(("current", first_key))

                # Add the sequence pair to the list
                sequences_list.append((first_key, second_key))

        # Write the file
        with open(output_file, 'w') as file:
            for col1, col2 in sequences_list:
                file.write(f"{col1} {col2}\n")

        print(f"File '{output_file}' created successfully.")

    def generate_input_files(self, end_current_system=0):

        self.generate_instance_dict()
        self.create_xpositions_file(end_current_system)
        self.create_sequences_file()
