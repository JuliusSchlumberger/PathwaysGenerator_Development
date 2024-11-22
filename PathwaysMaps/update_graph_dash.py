
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import os
import fnmatch
from scripts.main_central_path_directions import DIRECTORY_PATHWAYS_GENERATOR
from scripts.filter_options import ROBUSTNESS_METRICS_LIST, SCENARIO_OPTIONS
from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV, SCENARIOS_INV
from scripts.PathwaysMaps.create_pathways_maps_multi_risk import create_pathways_maps_multi_risk
from scripts.helperfunctions.add_line_breaks_axis_labels import add_line_breaks
from scripts.design_choices.main_dashboard_design_choices import FIG_DIMENSIONS, FONTS, LINE_WIDTH_LINE, LINE_WIDTH_MARKER, SIZE_MARKER, MAX_LINE_OFFSET
from scripts.design_choices.main_dashboard_dropdowns import ROH_DICT_INV
import json


def update_graph(pathway1, pathway2, pathway3, pathway4, scenario):
    scenarios_title = f'{SCENARIOS_INV[scenario]} climate scenario'
    planning_horizon = [2000, 2120]

    # Create a list of selected pathways
    all_pathways = [pathway1, pathway2, pathway3, pathway4]
    print('selected pathway numbers:', all_pathways)
    relevant_pathways = [p if p != 'not-considered' else 0 for p in all_pathways]
    # Identify the relevant sectors where the corresponding pathway is not 'not-considered'
    relevant_sectors = [sector for pathway, sector in zip(all_pathways, ROH_DICT_INV.keys()) if pathway != 'not-considered']

    complete_replace_dict = {}
    for risk_owner_hazard in ROH_DICT_INV.keys():
        complete_replace_dict[risk_owner_hazard] = {}
        with open(f'dynamic_data/data/renamed_pathways/renamed_pathways_{risk_owner_hazard}.json', 'r') as json_file:
            replace_dict = json.load(json_file)
        invert_replace_dict = {str(v): str(k) for k, v in replace_dict.items()}
        complete_replace_dict[risk_owner_hazard] = invert_replace_dict

    # Count how many pathways are "not-considered"
    not_considered_count = all_pathways.count('not-considered')

    # Filter out "not-considered" values
    selected_pathways = [p for p in all_pathways if p != 'not-considered']

    # Check if we need a single plot with two columns or subplots
    if not_considered_count >= 3 :
        return 'We need to consider multiple sector - risk pairs'

    if not_considered_count <= 1:
        cols = 2
    else:
        cols = 1

    figure = make_subplots(
        rows=2, cols=cols,  # Vertical stacking
        # shared_xaxes=True,  # Share x-axes across subplots
        subplot_titles=[f"{ROH_DICT_INV[relevant_sectors[i]]}: Focus on Pathway {p}" for i, p in enumerate(selected_pathways)],
        vertical_spacing=0.2,  # Adjust vertical spacing between rows (0-1)
        horizontal_spacing=0.05 if cols > 1 else 0  # No horizontal spacing for single column

    )

    # adding background plots without interactions

    tick = 0
    # Adding traces for each pathway
    for i, risk_owner_hazard in enumerate(ROH_DICT_INV.keys()):
        sector_pathway = relevant_pathways[i]
        if sector_pathway == 0:
            continue

        other_pathways = relevant_pathways[:i] + relevant_pathways[i+1:]
        other_sectors = [s for s in ROH_DICT_INV.keys() if s != risk_owner_hazard]
        row = tick // cols + 1  # Determine the row (1-based index)
        col = tick % cols + 1  # Determine the column (1-based index)
        print(risk_owner_hazard, sector_pathway, other_pathways, relevant_pathways, col, row)

        focus = f'{risk_owner_hazard}_{scenario}_average'
        line_choice = 'pathways'  # options: 'pathways', 'overlay', 'pathways_and_unique_lines'
        input_with_pathways = True  # True if input file contains pathway numbers
        ylabels = 'logos'  # options: 'logos', 'names', 'numbers'

        figure_title = f'Comparison of implementation timing in the system ({scenarios_title})'
        # create base figure as png and as plotly
        file_offset = f'{DIRECTORY_PATHWAYS_GENERATOR}/processed/{risk_owner_hazard}_optimized_offset'
        file_base = f'{DIRECTORY_PATHWAYS_GENERATOR}/processed/{risk_owner_hazard}_optimized_base'

        figure = create_pathways_maps_multi_risk(focus, line_choice, input_with_pathways, file_offset, file_base,
                             ylabels, planning_horizon, risk_owner_hazard,
                             sector_pathway, other_pathways, other_sectors, complete_replace_dict, row, col, figure, figure_title)

        figure.update_xaxes(
            tickvals=np.linspace(planning_horizon[0], planning_horizon[1], 7),
            ticktext = [''] + list(np.linspace(planning_horizon[0] + 20, planning_horizon[1], 6).astype(int).astype(str))
        )
        tick += 1


    figure.update_layout(
        title={'text': add_line_breaks(figure_title, 80), 'y': .95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom'},
        title_font_size=FONTS['title'],
        font_size=FONTS['main']-2,
        yaxis_title='',
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=70, b=5),
        # xaxis=dict(
        #     domain=[0.07, .76]  # Adjust x-axis domain
        # ),
        # yaxis=dict(
        #     domain=[0.2, .95]  # Adjust x-axis domain
        # ),
        width=FIG_DIMENSIONS['width']-20,  # Width set to 1300 pixels
        height=FIG_DIMENSIONS['height']-10,  # Height set to 600 pixels
        autosize=False,  # Disable autosizing to use the specified width and height
    )
    for annotation in figure['layout']['annotations']:
        annotation['font'] = dict(size=FONTS['main'])  # Set font size for all titles

    return figure



