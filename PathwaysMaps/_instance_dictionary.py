import numpy as np

def create_instance_dictionary(self, actions, instance_dict, initial_max_instance, x_position_dict):
    """
    Creates a dictionary mapping measures to their instances with unique numbers assigned to each instance.

    Parameters:
    - self: The class instance containing various configurations.
    - actions: Dict of actions with keys that include measure and instance information.
    - instance_dict: Dictionary to store instances of measures.
    - initial_max_instance: The initial maximum instance number before processing actions.
    - x_position_dict: Dictionary to store x-positions of measures.

    Returns:
    - instance_dict: Dictionary where each measure maps to another dictionary of instances with their unique numbers.
    - max_index: The highest instance number assigned across all measures.
    - x_position_dict: Updated dictionary of x-positions for each measure.
    """
    for key, value in actions.items():
        if key.startswith('ActionEnd'):
            # Split the key to extract measure and instance information
            parts = key.split('[')
            measure = parts[0].split('(')[1][1:]  # Extract measure part
            instance = parts[1].split(']')[0]  # Extract instance part
            x_position = value[0]  # Get the x-position from the value
            # print('inputs', measure, instance, x_position)
            if measure not in x_position_dict:
                x_position_dict[measure] = {}

            if self.line_choice == 'pathways_and_unique_lines' or self.line_choice == 'pathways':
                # Assign unique instance numbers to new x-positions
                if measure not in instance_dict:
                    instance_dict[measure] = {}
                    x_position_dict[measure][x_position] = 1  # Start instance numbering from 1
                else:
                    # Increment the instance number for a new x-position
                    if instance not in instance_dict[measure]:
                        if x_position not in x_position_dict[measure]:
                            new_index = max(x_position_dict[measure].values()) + 1
                        else:
                            new_index = max(x_position_dict[measure].values()) + 1
                        x_position_dict[measure][x_position] = new_index
                    else:
                        new_index = 0
                    if new_index > initial_max_instance:
                        initial_max_instance = new_index
            else:
                # Reuse instance numbers for x-positions that are close
                found = False
                for x_pos in x_position_dict[measure]:
                    if np.isclose(x_pos, x_position, atol=0.1):  # Check if positions are approximately the same
                        instance_number = x_position_dict[measure][x_pos]
                        found = True
                        break

                if not found:
                    # Assign a new instance number for a new x-position
                    if measure not in instance_dict:
                        instance_dict[measure] = {}
                        x_position_dict[measure][x_position] = 1  # Start instance numbering from 1
                    else:
                        # Increment the instance number for a new x-position
                        new_index = max(x_position_dict[measure].values()) + 1
                        x_position_dict[measure][x_position] = new_index

            # Assign the determined instance number to the instance
            # print('xpositions2', x_position_dict[measure])
            if instance not in instance_dict[measure]:  # Don't overwrite existing instance counts
                # instance_number = x_position_dict[measure].get(x_position, 0)
                instance_number = x_position_dict[measure][x_position]
                instance_dict[measure][instance] = instance_number  # Store the instance number in the dictionary
            # print('instance_dict', instance_dict)
    # Determine the maximum instance number across all measures
    max_index = 0
    for value in instance_dict.values():
        length = len(value)
        if length > max_index:
            max_index = length

    return instance_dict, max_index, x_position_dict  # Return the instance dictionary and the highest instance number assigned
