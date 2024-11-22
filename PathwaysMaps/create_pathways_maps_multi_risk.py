from scripts.design_choices.main_dashboard_design_choices import MEASURE_COLORS, MAX_X_OFFSET, MAX_Y_OFFSET
from scripts.map_system_parameters import INVERTED_MEASURE_NUMBERS, REPLACING_MEASURE, RENAMING_DICT
from scripts.main_central_path_directions import DIRECTORY_PATHWAYS_GENERATOR

from scripts.PathwaysMaps.pathways_generator_advanced import Pathways_Generator_Advanced

import json


def create_pathways_maps_multi_risk(focus, line_choice, input_with_pathways, file_offset, file_base,
                                    ylabels, planning_horizon, risk_owner_hazard,
                                    sector_pathway, other_pathways,other_sectors, complete_replace_dict, row, col, fig, figure_title):
    # Open text file for no interaction file
    file_tipping_points = f'{DIRECTORY_PATHWAYS_GENERATOR}/all_tp_timings_{focus}.txt'
    input_file_with_pathways = f'{DIRECTORY_PATHWAYS_GENERATOR}/all_sequences_{focus}.txt'
    file_sequence_only = f'{DIRECTORY_PATHWAYS_GENERATOR}/processed/all_sequences_{focus}_only_sequences.txt'

    NewPathwayMaps = Pathways_Generator_Advanced(
        MEASURE_COLORS, INVERTED_MEASURE_NUMBERS, REPLACING_MEASURE,
        line_choice=line_choice,
        input_with_pathways=input_with_pathways, fig=fig, col=col, row=row
    )

    renaming_dict = complete_replace_dict[risk_owner_hazard]

    # Create data for background plot
    data = NewPathwayMaps.create_start_files(
        input_file_with_pathways, file_sequence_only, file_tipping_points, renaming_dict, MAX_X_OFFSET, planning_horizon,
        basic=True
    )

    instance_dict, actions, action_transitions, \
    base_y_values, x_offsets, measures_in_pathways, \
    max_instance, base_y_offsets, x_position_dict_ini = data

    # Create data for selected pathway
    # print(other_pathways)
    other_pathways_old_names = []
    for p, s in zip(other_pathways, other_sectors):
        for key in complete_replace_dict[s].keys():
            if complete_replace_dict[s][key] == str(int(p)):
                other_pathways_old_names.append(key)
    print(risk_owner_hazard, sector_pathway, 'called and effective pathways', other_pathways, other_pathways_old_names)
    other_pathways_str = [str(p).zfill(2) for p in other_pathways_old_names]
    other_pathways_identifier = '&'.join(other_pathways_str)
    input_file_with_pathways_mr = f'{DIRECTORY_PATHWAYS_GENERATOR}/multi_risk/all_sequences_{focus}_{other_pathways_identifier}.txt'
    file_sequence_only_mr = f'{DIRECTORY_PATHWAYS_GENERATOR}/processed/all_sequences_{focus}_{other_pathways_identifier}_only_sequences.txt'
    file_tipping_points_mr = f'{DIRECTORY_PATHWAYS_GENERATOR}/multi_risk/all_tp_timings_{focus}_{other_pathways_identifier}.txt'

    # Create data for spotlight plot
    interaction_data = NewPathwayMaps.create_start_files(
        input_file_with_pathways_mr,
        file_sequence_only_mr,
        file_tipping_points_mr,
        renaming_dict,
        MAX_X_OFFSET,
        planning_horizon,
        False,   # measures_in_pathways
        base_y_values,
        instance_dict,
        max_instance,
        x_position_dict_ini,
        sector_pathway
    )

    instance_dict, actions_i, action_transitions_i, \
    base_y_values, x_offsets, measures_in_pathways_i, \
    max_instance, base_y_offsets, _ = interaction_data

    
    # Load optimized positions
    with open(f'{file_offset}.json', 'r') as file:
        preferred_offset = json.load(file)

    with open(f'{file_base}.json', 'r') as file:
        preferred_base = json.load(file)

    # Create markers
    action_pairs, data, preferred_dict_inv = NewPathwayMaps.create_markers(
        actions, instance_dict, preferred_offset, preferred_base, measures_in_pathways, line_choice
    )

    # Create markers for spotlight
    action_pairs_i, data_i, preferred_dict_inv = NewPathwayMaps.create_markers(
        actions_i, instance_dict, preferred_offset, preferred_base, measures_in_pathways_i, line_choice
    )

    NewPathwayMaps.pathways_plotly_with_background(
        data_i, action_pairs_i, action_transitions_i, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
        measures_in_pathways_i, measures_in_pathways, planning_horizon, risk_owner_hazard, figure_title, ylabels, color='#d9d9d9'
    )
    # fig.show()
    return NewPathwayMaps.figure
