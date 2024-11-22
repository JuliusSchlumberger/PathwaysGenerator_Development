import numpy as np

from adaptation_pathways.graph import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)
from adaptation_pathways.plot.pathway_map.classic import _layout as pathway_layout
from PathwaysMaps._get_first_measures_for_offset import get_first_measures_for_offset


def replace_strings_in_list(lst, replacements):
    """
    Recursively replaces strings in a list based on a replacement dictionary.

    Parameters:
    - lst: The list containing strings and other elements.
    - replacements: A dictionary where keys are substrings to be replaced, and values are the replacements.

    Returns:
    - new_list: A new list with strings replaced according to the replacements dictionary.
    """

    if not isinstance(lst, list):
        return lst  # If lst is not a list, return it as is

    new_list = []
    for item in lst:
        if isinstance(item, dict):
            new_list.append(replace_strings_in_dict_keys(item, replacements))  # Handle nested dictionaries
        elif isinstance(item, list):
            new_list.append(replace_strings_in_list(item, replacements))  # Handle nested lists
        elif isinstance(item, str):
            new_item = item
            for old, new in replacements.items():
                new_item = new_item.replace(old, new)  # Replace substrings
            new_list.append(new_item)
        else:
            new_list.append(item)  # Append non-string items unchanged
    return new_list

def replace_strings_in_dict_keys(d, replacements):
    """
    Recursively replaces strings in dictionary keys based on a replacement dictionary.

    Parameters:
    - d: The dictionary containing keys to be processed.
    - replacements: A dictionary where keys are substrings to be replaced, and values are the replacements.

    Returns:
    - new_dict: A new dictionary with keys replaced according to the replacements dictionary.
    """
    if not isinstance(d, dict):
        return d  # If d is not a dictionary, return it as is

    new_dict = {}
    for k, v in d.items():
        new_key = k
        for old, new in replacements.items():
            new_key = new_key.replace(old, new)  # Replace substrings in keys
        if isinstance(v, dict):
            new_dict[new_key] = replace_strings_in_dict_keys(v, replacements)  # Handle nested dictionaries
        elif isinstance(v, list):
            new_dict[new_key] = replace_strings_in_list(v, replacements)  # Handle nested lists
        else:
            new_dict[new_key] = v  # Append values unchanged
    return new_dict

def get_sequences_only(input_file, file_sequence_only, renaming_dict, sector_pathway, basic):
    """
    Extracts sequences and pathways from an input file, and renames measures based on a renaming dictionary.

    Parameters:
    - input_file: Path to the input file containing sequences.
    - file_sequence_only: Path to save the extracted sequences only.
    - renaming_dict: A dictionary for renaming measures.

    Returns:
    - measures_in_pathways: A dictionary mapping pathways to their associated measures.
    """
    print(input_file)
    with open(input_file, 'r') as file:
        all_lines = file.readlines()  # Read all lines from the file
    full_input = [item.split(' ') for item in all_lines]  # Split lines into components
    split_lines = [item.split(' ')[:2] for item in all_lines]  # Extract first two columns
    pathways = [item.split(' ')[-1].replace('\n', '').split(';') for item in all_lines]  # Extract pathways

    if sector_pathway:  # spotlight one pathway
        for key in renaming_dict.keys():
            if renaming_dict[key] == str(int(sector_pathway)):
                original_name = key

        unique_pathways = [str(int(sector_pathway))]
    else:
        unique_flat_list = list(set(item for sublist in pathways for item in sublist))
        unique_pathways = [renaming_dict.get(key, key) for key in unique_flat_list]

    measures_in_pathways = {pathway: set() for pathway in unique_pathways}
    for pathway in unique_pathways:
        for sublist in full_input:
            pw_list = [renaming_dict.get(key, key) for key in sublist[2].replace('\n', '').split(';')]
            clean_ps = [int(p) for p in pw_list]
            if int(pathway) in clean_ps:
                measures_in_pathways[pathway].add(sublist[0])
                measures_in_pathways[pathway].add(sublist[1])
        measures_in_pathways[pathway] = list(measures_in_pathways[pathway])
    measures_in_pathways = replace_strings_in_dict_keys(measures_in_pathways, renaming_dict)

    if sector_pathway:
        # Step 1: Find indices where sector_pathway is present in pathways
        indices = [i for i, path in enumerate(pathways) if original_name in path]

        # Step 2: Extract elements from 'full' using these indices
        split_lines = [split_lines[i] for i in indices]

    if basic:
        pass
    else:
        sequences_only = [' '.join(item) + '\n' for item in split_lines]
        with open(file_sequence_only, 'w') as new_file:
            for item in sequences_only:
                new_file.write(item)  # Write the sequences to a new file
        new_file.close()  # Ensure the file is closed
    return measures_in_pathways

def get_pathway_map(sequences_txt, tipping_points_txt):
    """
    Generates a pathway map from sequences and tipping points.

    Parameters:
    - sequences_txt: Path to the file containing sequences.
    - tipping_points_txt: Path to the file containing tipping points.

    Returns:
    - pathway_map: A pathway map object with assigned tipping points and levels.
    """
    sequences = read_sequences(sequences_txt)  # Read sequences from the file
    sequence_graph = sequences_to_sequence_graph(sequences)  # Create a sequence graph
    level_by_action = action_level_by_first_occurrence(sequences)  # Determine action levels
    pathway_map = sequence_graph_to_pathway_map(sequence_graph)  # Convert to pathway map

    tipping_points = read_tipping_points(tipping_points_txt, pathway_map.actions())
    pathway_map.assign_tipping_points(tipping_points)  # Assign tipping points to the map
    pathway_map.set_attribute("level", level_by_action)  # Set levels in the pathway map

    # _, axes = plt.subplots(layout="constrained")
    # init_axes(axes)
    # plot(axes, pathway_map)
    # plt.show()

    return pathway_map

def clean_list(lst):
    """
    Cleans up strings in a list by removing specific characters and converting pure numbers to integers.

    Parameters:
    - lst: List of strings to be cleaned.

    Returns:
    - cleaned_list: List with cleaned and converted elements.
    """
    cleaned_list = []
    for item in lst:
        cleaned_item = item.replace('"', "").replace(")", "").replace("((", "")
        if cleaned_item.strip().isdigit():
            cleaned_list.append(int(cleaned_item.strip()))  # Convert to integer if it's a number
        else:
            cleaned_list.append(cleaned_item.strip())  # Strip whitespace from non-numbers
    return cleaned_list

def generate_unique_offsets_with_zero(keys, max_offset):
    """
    Generates unique offsets for a list of keys, ensuring that zero is included in the offsets.

    Parameters:
    - keys: List of keys to generate offsets for.
    - max_offset: Maximum absolute value for the offsets.

    Returns:
    - offset_dict: Dictionary mapping keys to their unique offsets.
    """

    num_keys = len(keys)
    offsets = np.linspace(-max_offset, max_offset, num_keys)  # Generate evenly spaced offsets

    if 0 not in offsets:
        closest_to_zero_idx = np.argmin(np.abs(offsets))
        offsets[closest_to_zero_idx] = 0.0  # Ensure zero is included
        offsets = np.sort(offsets)  # Re-sort the offsets

    offset_dict = {key: offset for key, offset in zip(keys, offsets)}
    return offset_dict

def get_network_dicts(self, input_file, file_sequence_only, file_tipping_points, max_offset, planning_horizon, sector_pathway, basic):
    """
    Generates network dictionaries and layouts from input files and renaming parameters.

    Parameters:
    - input_file: Path to the input file containing sequences.
    - file_sequence_only: Path to save the extracted sequences only.
    - file_tipping_points: Path to the file containing tipping points.
    - max_offset: Maximum absolute value for the offsets.
    - self.with_pathways: Boolean indicating whether pathways information is included.

    Returns:
    - pw_layout_renamed: Dictionary representing the renamed pathway layout.
    - edge_list_renamed: List of renamed edges for the network.
    - base_y_values_renamed: Dictionary of renamed base y-values for measures.
    - x_offsets: Dictionary of unique offsets for each measure.
    - measures_in_pathways: Dictionary mapping pathways to their associated measures.
    """
    if self.input_with_pathways:
        measures_in_pathways = get_sequences_only(input_file, file_sequence_only, self.renaming_dict, sector_pathway, basic)
    else:
        measures_in_pathways = 'No information about different pathways provided.'
    pathway_map = get_pathway_map(file_sequence_only, file_tipping_points)
    pw_layout = pathway_layout(pathway_map)
    pw_layout_repr = {repr(key): value for key, value in pw_layout.items()}

    pw_layout_renamed = replace_strings_in_dict_keys(pw_layout_repr, self.renaming_dict)

    for_ybasevalues = {str(key): value for key, value in pw_layout.items()}
    base_y_values = {}
    for key, value in for_ybasevalues.items():
        if key.startswith('['):
            base_y_values[key[1:]] = value[1]
    base_y_values_renamed = replace_strings_in_dict_keys(base_y_values, self.renaming_dict)

    x_offsets = generate_unique_offsets_with_zero(base_y_values_renamed.keys(), max_offset)

    edge_list = []
    for edge in pathway_map.graph.edges.items():
        repr_edge = repr(edge).replace('((', '').replace('), {})', '').split(',')
        repr_edge = clean_list(repr_edge)
        edge_list.append(repr_edge)

    edge_list_renamed = replace_strings_in_list(edge_list, self.renaming_dict)

    base_y_offsets = get_first_measures_for_offset(edge_list_renamed)

    pw_layout_renamed['ActionBegin("0[0]")'][0] = planning_horizon[0] - 20

    return pw_layout_renamed, edge_list_renamed, base_y_values_renamed, x_offsets, measures_in_pathways, base_y_offsets