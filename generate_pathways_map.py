from PathwaysMaps.create_pathways_maps import create_pathways_maps
from case_study_information import MEASURE_NUMBERS, INVERTED_MEASURE_NUMBERS, MEASURE_DICT, RENAMING_DICT
from PathwaysMaps._create_colors import MEASURE_COLORS, BASE_COLORS_SECTORS



unique_identifier = 'TTT'
risk_owner_hazard = 'flood_agr' # alternatives: 'drought_agr', 'flood_urb', 'flood_agr'
scenario = 'Wp' # alternatives: 'Wp', 'D', 'G'
planning_horizon = [2020,2120]


file_sequence_with_pathway = f'data/inputs/all_sequences_{risk_owner_hazard}_{scenario}_average.txt'    # This input file looks slightly different from the original sequence. I added an extra column to add specifiers for columns. It would take me too much time to adjust this now, so I kept it.
file_tipping_points = f'data/inputs/all_tp_timings_{risk_owner_hazard}_{scenario}_average.txt'
file_sequence_only = f'data/inputs/processed/all_sequences_{risk_owner_hazard}_{scenario}_only_sequences.txt'   # this file will be generated

# if considering interactions
interaction_identifier = False # alternative: identifier_for_interactions or False. If False, no interactions considered
interacting_sector_string = 'flood_agr&drought_agr'    # any combination of the risk_owner_hazard. Note: order is relevant (check data/inputs/interactions)
input_file_for_interactions = f'data/inputs/interactions/all_sequences_{risk_owner_hazard}_{scenario}_average_{interacting_sector_string}'

visualization_output_plot = f'pathways_map_{risk_owner_hazard}_{scenario}_{unique_identifier}' if interaction_identifier else f'pathways_map_{risk_owner_hazard}_{scenario}'


# create base figure as png and as plotly
file_offset = f'data/inputs/processed/{risk_owner_hazard}_optimized_offset'
file_base = f'data/inputs/processed/{risk_owner_hazard}_optimized_base'


# Design Choices
line_choice = 'pathways_and_unique_lines'  # options: 'pathways', 'overlay', 'pathways_and_unique_lines'
input_with_pathways = True  # True if input file contains pathway numbers
optimize_marker_positions = False  # Specifies whether to optimize 'both', 'offset', or 'base_y' positions. Or False to not optimize
num_iterations = 'all'  # options: number (int) to specify number of iterations for optimization or 'all' to consider all possible combinations for optimization
ylabels = 'logos'  # options: 'logos', 'names', 'numbers'
plot_type = 'matplotlib' # alternatives: 'plotly', 'matplotlib'


max_x_offset = .7 # will do adjustments in horizontal direction. Needs adjustment if lines of different measures start overlap.
max_y_offset = .48 # will do adjustments in vertical direction between instances. Needs adjustment if markers overlap.

fonts = {
    "annotations": 12,
    'main': 12,
    'title': 15
}

fig_dimensions = {
    'width': 1300,
    'height': 1000
}

line_width_marker = 2
size_marker = 35
line_width_line = 2
max_line_offset = 0.2


figure_title = f'Pathways Map ({unique_identifier})'

create_pathways_maps(line_choice, input_with_pathways, file_offset, file_base, ylabels, planning_horizon,
                     risk_owner_hazard, figure_title, file_tipping_points, file_sequence_with_pathway,
                     file_sequence_only, MEASURE_NUMBERS, INVERTED_MEASURE_NUMBERS, MEASURE_COLORS,
                     max_x_offset, max_y_offset, fonts, fig_dimensions, line_width_marker, size_marker,line_width_line,
                     max_line_offset,
                     plot_type,
                     visualization_output_plot,
                     BASE_COLORS_SECTORS,
                     MEASURE_DICT, RENAMING_DICT,
                     optimize_marker_positions, num_iterations,
                     interaction_identifier, input_file_for_interactions)
