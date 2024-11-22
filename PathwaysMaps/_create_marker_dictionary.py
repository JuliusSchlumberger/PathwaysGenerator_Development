import numpy as np


def get_closest_instance(y_offsets, measure, instance, max_search_range=5):
    # First, check if the exact instance exists
    if str(instance) in y_offsets[measure]:
        return y_offsets[measure][str(instance)]

    # If the exact instance is not found, start searching for the closest match
    for offset in range(0, max_search_range + 1):
        # Check instance + offset
        if str(int(instance) + offset) in y_offsets[measure]:
            return y_offsets[measure][str(int(instance) + offset)]

        # Check instance - offset
        if str(int(instance) - offset) in y_offsets[measure]:
            return y_offsets[measure][str(int(instance) - offset)]

    # If no match is found within the search range, return a default or raise an exception
    raise KeyError(f"Instance {instance} and nearby instances not found in measure '{measure}'")


def create_marker_dictionary(self, actions, base_y_values, instance_dict, y_offsets, measures_in_pathways, line_choice):
    """
    Processes musical actions to create dictionaries for plotting and line drawing.

    Parameters:
    - self: The class instance containing various configurations.
    - actions: Dict of action data keyed by composite identifiers including measure and instance.
    - base_y_values: Dict mapping measure identifiers to base y-values.
    - instance_dict: Dict mapping measures to another dict that maps instances to unique numbers.
    - y_offsets: Dict mapping unique instance numbers to y-offsets for vertical positioning.
    - measures_in_pathways: Dict mapping pathways to their associated measures.

    Returns:
    - action_pairs: Dict for storing Begin and End coordinates by measure and instance.
    - data: Organized list of tuples containing adjusted y-values, markers, colors, and face colors for plotting.
    """

    action_pairs = {}  # Stores the coordinate pairs for drawing lines between points.
    data = {}  # Stores visual plotting data organized by measure.

    # Iterate through each action to parse and process its components
    for key, value in actions.items():
        parts = key.split('[')  # Split the key to extract measure and instance information
        measure = parts[0].split('(')[1][1:]  # Extract measure part
        instance = parts[1].split(']')[0]  # Extract instance part
        base_y = base_y_values.get(measure, 0)  # Get base y-value for the measure, default to 0

        # Setup marker styles and colors based on action type
        marker = 'o'
        action_type = "Begin" if "Begin" in key else "End"
        color = self.measure_colors[str(measure)]  # Color for the measure
        facecolor = 'w' if "End" in key else color  # Hollow for "End", filled for "Begin"

        # Adjust y-value based on the instance's unique number and its offset
        if len(instance_dict[measure]) < 2 or all(value == 1 for value in instance_dict[measure].values()) or line_choice=='overlay':
            # Make sure that measures where we only have one instance have no offset
            y_adjustment = 0
        else:
            # print(measure, y_offsets)
            try:
                y_adjustment = get_closest_instance(y_offsets, measure, instance)
            except KeyError as e:
                print(e)
        value_adjusted = np.array([value[0], int(base_y) + y_adjustment])  # Adjust y-value

        # Information on pathways_number
        if measure == '0':
            pathways_with_measure_instance = [key for key, array in measures_in_pathways.items() if f'{measure}' in array]
        else:
            pathways_with_measure_instance = [key for key, array in measures_in_pathways.items() if f'{measure}[{instance}]' in array]

        # Organize data by measure for plotting
        if measure not in data:
            data[measure] = []
        data[measure].append((value_adjusted, marker, color, facecolor, pathways_with_measure_instance))

        # Prepare action_pairs for line drawing
        coord_key = (measure, instance)
        if coord_key not in action_pairs:
            action_pairs[coord_key] = {}
        action_pairs[coord_key][action_type] = value_adjusted
    return action_pairs, data  # Return the dictionaries for plotting and drawing



def create_marker_dictionary_optimization(actions, base_y_values, y_offsets):
    action_pairs = {}
    # Parse the keys to organize data
    data = {}
    # print(base_y_values)
    for key, value in actions.items():
        parts = key.split('[')
        measure = parts[0].split('(')[1][1:]
        instance = parts[1].split(']')[0]

        base_y = base_y_values.get(measure, 0)  # Default to 0 if measure not in base_y_values

        marker = 'o'
        action_type = "Begin" if "Begin" in key else "End"

        # Adjust y-values slightly based on instance (unique measure-instance combination)
        if measure != '0':
            y_adjustment = y_offsets[measure][str(instance)]
        else:
            y_adjustment = 0
        value_adjusted = np.array([value[0], int(base_y) + y_adjustment])

        # Store in data dictionary
        if measure not in data:
            data[measure] = []
        data[measure].append((value_adjusted, marker))

        # Prepare coordinates for line drawing
        coord_key = (measure, instance)
        if coord_key not in action_pairs:
            action_pairs[coord_key] = {}
        action_pairs[coord_key][action_type] = value_adjusted
    return action_pairs, data
