
from PathwaysMaps.pathways_generator_advanced import Pathways_Generator_Advanced
from PathwaysMaps.jsonscript import HOVER_JS

import json


def create_pathways_maps(line_choice, input_with_pathways, file_offset, file_base,ylabels, planning_horizon,
                     risk_owner_hazard, figure_title, file_tipping_points,file_sequence_with_pathway,
                     file_sequence_only, measure_numbers, inverted_measure_numbers, measure_colors,
                     max_x_offset, max_y_offset, fonts, fig_dimensions, line_width_marker, size_marker, line_width_line, max_line_offset,
                     plot_type,
                     visualization_output_plot,
                     base_colors_sectors,
                     measure_dict, renaming_dict,
                         optimize_marker_positions=False, num_iterations='both',
                     interaction_identifier=False, input_file_for_interactions=False):

    NewPathwayMaps = Pathways_Generator_Advanced(
        measure_colors, base_colors_sectors, inverted_measure_numbers, {}, line_choice,
        max_y_offset, fonts, fig_dimensions, line_width_marker, size_marker, line_width_line, max_line_offset,
        measure_numbers, inverted_measure_numbers, measure_dict, renaming_dict,
        input_with_pathways, plot_type
    )

    # Needed to rename pathways (left-over from Dashboard context)
    with open(f'data/renamed_pathways/renamed_pathways_{risk_owner_hazard}.json', 'r') as json_file:
        replace_dict = json.load(json_file)
    renaming_dict = {str(v): str(k) for k, v in replace_dict.items()}

    # Create data for no-interaction plot
    data = NewPathwayMaps.create_start_files(
        file_sequence_with_pathway, file_sequence_only, file_tipping_points, renaming_dict, max_x_offset, planning_horizon,
    )

    instance_dict, actions, action_transitions, \
    base_y_values, x_offsets, measures_in_pathways, \
    max_instance, base_y_offsets, x_position_dict_ini = data

    # I load here two different data-set's and need to do some extension of the set of sequences, instances for the offsetting and positioning of pathways.
    if interaction_identifier:
        input_file_with_pathways_with_interaction = f'{input_file_for_interactions}.txt'
        file_sequence_only_with_interaction = f'{input_file_for_interactions}_only_sequences.txt'
        file_tipping_points_with_interaction = f'{input_file_for_interactions.replace("all_sequences", "all_tp_timings")}.txt'

        # Create data for interaction plot
        interaction_data = NewPathwayMaps.create_start_files(
            input_file_with_pathways_with_interaction,
            file_sequence_only_with_interaction,
            file_tipping_points_with_interaction,
            renaming_dict,
            max_x_offset,
            planning_horizon,
            False,   # measures_in_pathways
            base_y_values,
            instance_dict,
            max_instance,
            x_position_dict_ini
        )

        instance_dict, actions_i, action_transitions_i, \
        base_y_values, x_offsets, measures_in_pathways_i, \
        max_instance, base_y_offsets, _ = interaction_data

    if optimize_marker_positions:
        NewPathwayMaps.optimize_positions(instance_dict, actions, action_transitions, base_y_values, max_instance, base_y_offsets,
                           max_y_offset,
                           file_offset, file_base, num_iterations, optimize_marker_positions)

    # Load optimized positions
    with open(f'{file_offset}.json', 'r') as file:
        preferred_offset = json.load(file)

    with open(f'{file_base}.json', 'r') as file:
        preferred_base = json.load(file)

    # Create markers
    action_pairs, data, preferred_dict_inv = NewPathwayMaps.create_markers(
        actions, instance_dict, preferred_offset, preferred_base, measures_in_pathways, line_choice
    )
    if interaction_identifier:
        # Create markers with interactions
        action_pairs_i, data_i, preferred_dict_inv = NewPathwayMaps.create_markers(
            actions_i, instance_dict, preferred_offset, preferred_base, measures_in_pathways_i, line_choice
        )
    # Generate and save the base figure without interactions

    if interaction_identifier:
        if plot_type == 'plotly':
            fig = NewPathwayMaps.pathways_plotly_with_background(
                data_i, action_pairs_i, action_transitions_i, data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                measures_in_pathways_i, measures_in_pathways, planning_horizon, risk_owner_hazard, figure_title, ylabels, color='#d9d9d9'
            )

            # Write the plot to an HTML file
            fig.write_html(f'{visualization_output_plot}_{interaction_identifier}.html', include_plotlyjs='cdn')

            # # Append custom JavaScript for hover behavior
            # fig_json = fig.to_plotly_json()
            # # Add the custom JavaScript to the JSON structure
            # # fig_json['custom_js'] = HOVER_JS
            #
            # with open(f'{savepath}.json', 'w') as f:
            #     json.dump(fig_json, f)
        elif plot_type == 'matplotlib':
            fig = NewPathwayMaps.create_base_figure(data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                           measures_in_pathways, planning_horizon, ylabels)
            fig = NewPathwayMaps.add_other_map(data_i, action_pairs_i, action_transitions_i, x_offsets, preferred_dict_inv,
                                         measures_in_pathways_i, planning_horizon, ylabels)

            fig.savefig(f'{visualization_output_plot}_{interaction_identifier}.png', dpi=300)

    else:
        if plot_type == 'plotly':
            fig = NewPathwayMaps.create_base_figure_plotly(
                data, action_pairs, action_transitions, x_offsets, preferred_dict_inv,
                measures_in_pathways, planning_horizon, risk_owner_hazard, figure_title, ylabels=ylabels
            )

            # Write the plot to an HTML file
            fig.write_html(f'{visualization_output_plot}.html', include_plotlyjs='cdn')

            # # Append custom JavaScript for hover behavior
            # fig_json = fig.to_plotly_json()
            # # Add the custom JavaScript to the JSON structure
            # # fig_json['custom_js'] = HOVER_JS
            #
            # with open(f'{savepath}.json', 'w') as f:
            #     json.dump(fig_json, f)
        elif plot_type == 'matplotlib':
            fig = NewPathwayMaps.create_base_figure(data, action_pairs, action_transitions, x_offsets,
                                                    preferred_dict_inv,
                                                    measures_in_pathways, planning_horizon, ylabels)
            fig.savefig(f'{visualization_output_plot}.png', dpi=300)
