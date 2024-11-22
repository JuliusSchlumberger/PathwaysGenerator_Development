import numpy as np
import plotly.graph_objects as go
from PathwaysMaps._find_integers import find_first_and_second_integers

from PathwaysMaps._helper_functions import image_to_base64, add_line_breaks



def base_figure_plotly(self, data, action_pairs, action_transitions, offsets, preferred_dict_inv, measures_in_pathways, planning_horizon, figure_title, ylabels,risk_owner_hazard):
    """
    Creates the base figure for the pathways map using Plotly.

    Parameters:
    - self: The class instance containing various configurations.
    - data: Dict containing plotting data organized by measure.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - action_transitions: List of transitions between actions.
    - offsets: Dict of offsets for measures.
    - preferred_dict_inv: Dict for measure button mappings.
    - measures_in_pathways: Dict of measures in each pathway.
    - ylabels: String whether to add logos, names or numbers to the plot.

    Returns:
    - fig: The Plotly figure with the base pathways map.
    """

    fig = self.figure

    # Add horizontal lines to the plot
    fig = add_horizontal_lines(self, fig, action_pairs, measures_in_pathways, self.line_choice, self.replacing_measure, self.measure_colors, risk_owner_hazard)

    # Add vertical lines to the plot
    fig = add_vertical_lines(self, fig, action_transitions, action_pairs, measures_in_pathways, offsets, self.line_width_line, self.measure_colors, risk_owner_hazard)

    # Add markers to the plot
    fig = add_actions(self, fig, data, self.line_width_marker, self.size_marker, risk_owner_hazard)

    # Optionally add measure logos to the plot
    if ylabels == 'logos':
        fig = add_measure_buttons_plotly(self, fig, preferred_dict_inv, planning_horizon, risk_owner_hazard)

    # Update layout with titles and hover mode
    fig.update_layout(
        title={'text': add_line_breaks(figure_title, 80), 'y': .95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom'},
        title_font_size=self.fonts['title'],
        font_size=self.fonts['main'],
        xaxis_title='Years',
        yaxis_title='',
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=5, r=5, t=30, b=5),
        xaxis=dict(
            domain=[0.07, .76]  # Adjust x-axis domain
        ),
        yaxis=dict(
            domain=[0.2, .95]  # Adjust x-axis domain
        ),
        width=self.fig_dimensions['width'],  # Width set to 1300 pixels
        height=self.fig_dimensions['height'],  # Height set to 600 pixels
        autosize=False,  # Disable autosizing to use the specified width and height
    )
    fig.update_xaxes({'range': (planning_horizon[0], planning_horizon[1]), 'autorange': False})

    # Add an image under the legend to the left
    base64_image = image_to_base64(f'data/legends/colorized/vertical_{risk_owner_hazard}_full_legend.png')
    fig.add_layout_image(
        dict(
            source=base64_image,
            # Replace with your image URL or path
            x=1,  # Adjust x position (slightly right of the legend)
            y=.5,  # Adjust y position
            xref="paper",
            yref="paper",
            sizex=.6,  # Adjust size of the image
            sizey=.6,
            xanchor="right",
            yanchor="middle"
        )
    )

    # Update the y-axis to hide the y-ticks
    fig.update_yaxes(showticklabels=False)

    return fig

def pathways_plotly_with_background(self, data_new, action_pairs_new, action_transitions_new, data_old,
                                    action_pairs_old, action_transitions_old, offsets, preferred_dict_inv,
                                    measures_in_pathways_new, measures_in_pathways_old, planning_horizon,
                                    risk_owner_hazard, figure_title, ylabels, color):
    """
    Creates the pathways change figure using Plotly, highlighting changes between two scenarios for the same set of pathways.

    Parameters:
    - self: The class instance containing various configurations.
    - data_new: Dict containing plotting data to be highlighed organized by measure.
    - action_pairs_new: Dict containing the start and end coordinates of actions to be highlighed.
    - action_transitions_new: List of transitions between actions to be highlighed.
    - data_old: Dict containing plotting data for reference organized by measure.
    - action_pairs_old: Dict containing the start and end coordinates of actions for reference.
    - action_transitions_old: List of transitions between actions for reference.
    - offsets: Dict of offsets for measures.
    - preferred_dict_inv: Dict for measure button mappings.
    - measures_in_pathways: Dict of measures in each pathway.
    - ylabels: String whether to add logos, names or numbers to the plot.

    Returns:
    - fig: The Plotly figure with the pathways change map.
    """

    fig = self.figure
    col = self.col
    row = self.row

    # Add old pathways (colored grey)
    fig = add_horizontal_lines(self, fig, action_pairs_old, measures_in_pathways_old, self.line_choice, self.replacing_measure, self.measure_colors, risk_owner_hazard, color, other_pathways=True, col=col, row=row)
    fig = add_vertical_lines(self, fig, action_transitions_old, action_pairs_old, measures_in_pathways_old, offsets, self.line_width_line, self.measure_colors, risk_owner_hazard, color, other_pathways=True, col=col, row=row)
    fig = add_actions(self, fig, data_old, self.line_width_marker, self.size_marker, risk_owner_hazard, color, other_pathways=True, change_plot=True, col=col, row=row)

    # Add new pathways
    fig = add_horizontal_lines(self, fig, action_pairs_new, measures_in_pathways_new, self.line_choice, self.replacing_measure, self.measure_colors, risk_owner_hazard, col=col, row=row)
    fig = add_vertical_lines(self, fig, action_transitions_new, action_pairs_new, measures_in_pathways_new, offsets, self.line_width_line, self.measure_colors, risk_owner_hazard, col=col, row=row)
    fig = add_actions(self, fig, data_new, self.line_width_marker, self.size_marker, risk_owner_hazard, change_plot=True, col=col, row=row)

    # Optionally add measure logos to the plot
    if ylabels == 'logos':
        fig = add_measure_buttons_plotly(self, fig, preferred_dict_inv,planning_horizon, risk_owner_hazard, col=col, row=row)

    if col == None and row == None: # normal plot
        fig.update_layout(
            title={'text': add_line_breaks(figure_title, 80), 'y': .95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'bottom'},
            title_font_size=self.fonts['title'],
            font_size=self.fonts['main'],
            xaxis_title='Years',
            yaxis_title='',
            showlegend=False,
            hovermode='closest',
            plot_bgcolor='white',
            margin=dict(l=5, r=5, t=30, b=5),
            xaxis=dict(
                domain=[0.07, .76]  # Adjust x-axis domain
            ),
            yaxis=dict(
                domain=[0.2, .95]  # Adjust x-axis domain
            ),
            width=self.fig_dimensions['width'],  # Width set to 1300 pixels
            height=self.fig_dimensions['height'],  # Height set to 600 pixels
            autosize=False,  # Disable autosizing to use the specified width and height
        )

        # Add an image under the legend to the left
        base64_image = image_to_base64(f'data/legends/{risk_owner_hazard}/colorized/vertical_{risk_owner_hazard}_full_legend.png')
        fig.add_layout_image(
            dict(
                source=base64_image,
                # Replace with your image URL or path
                x=1,  # Adjust x position (slightly right of the legend)
                y=.5,  # Adjust y position
                xref="paper",
                yref="paper",
                sizex=.6,  # Adjust size of the image
                sizey=.6,
                xanchor="right",
                yanchor="middle"
            )
        )

    fig.update_xaxes({'range': (planning_horizon[0], planning_horizon[1]), 'autorange': False})
    # Update the y-axis to hide the y-ticks
    fig.update_yaxes(showticklabels=False)

    return fig

def add_actions(self, fig, data, line_width_marker, size_marker, risk_owner_hazard, color='grey', other_pathways=False, change_plot=False, col = None, row = None):
    """
    Adds action markers to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add markers to.
    - data: Dict containing plotting data organized by measure.
    - line_width_marker: Width of the marker lines.
    - size_marker: Size of the markers.
    - other_pathways: Boolean indicating whether the markers belong to other pathways (colored grey).

    Returns:
    - fig: The Plotly figure with added action markers.
    """
    for measure, points in data.items():
        for point in points:
            x, y = point[0]
            first_part = f"<b>Pathway {point[4][0]}</b>" if len(
                point[4]) == 1 else f"<b>Pathways {', '.join(point[4])}</b>"
            second_part = f': ' if change_plot == False else f' (no interactions): ' if other_pathways else f' (with interactions): '
            third_part = f"'{self.measure_dict[self.inverted_measure_numbers[int(measure)]]}' implemented as new measure in year {int(x)}" if point[3] != 'w' \
                else f"Tipping point reached in year {int(x)}: current measures not sufficient anymore."
            hover_text = (
                first_part + second_part + third_part
            )

            symbol = 'circle'

            if col == None and row == None:
                facecolor = 'white' if point[3] == 'w' else color if other_pathways else point[3]
                marker = dict(
                    symbol=symbol,
                    size=size_marker,
                    color=facecolor,
                    line=dict(color=color if other_pathways else point[2], width=line_width_marker)
                )
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=marker,
                    showlegend=False,
                    customdata=[point[4]],  # Full list of groups for each point without additional nesting
                    text=hover_text,  # Display the pathways correctly
                    hovertemplate="%{x}<extra></extra>",  # Ensure text is used in hover data
                    # hoverinfo='none',  # Disable default hover info on the plot
                    # hovertemplate = hover_text,
                ))
            else:
                facecolor = 'white' if point[3] == 'w' else color if other_pathways else self.base_colors_sectors[risk_owner_hazard]
                marker = dict(
                    symbol=symbol,
                    size=size_marker-5,
                    color=facecolor,
                    line=dict(color=color if other_pathways else self.base_colors_sectors[risk_owner_hazard], width=line_width_marker)
                )
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    marker=marker,
                    showlegend=False,
                    customdata=[point[4]],  # Full list of groups for each point without additional nesting
                    # text=hover_text,  # Display the pathways correctly
                    hovertemplate=hover_text,  # Ensure text is used in hover data
                    hoverinfo='none',  # Disable default hover info on the plot
                    # hovertemplate = hover_text,
                ), row=row, col=col)
    return fig

def add_horizontal_lines(self, fig, action_pairs, measures_in_pathways, line_choice, replacing_measure, measure_colors, risk_owner_hazard, color='grey',  other_pathways=False, col=None, row=None):
    """
    Adds horizontal lines to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add lines to.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - measures_in_pathways: Dict of measures in each pathway.
    - line_choice: Indicating whether different pathways are drawn with unique lines for active measures or just overlaid
    - replacing_measure: Dict of measures being replaced.
    - measure_colors: Dict mapping measures to their colors.
    - other_pathways: Boolean indicating whether the lines belong to other pathways (colored grey).

    Returns:
    - fig: The Plotly figure with added horizontal lines.
    """

    if line_choice == 'pathways_and_unique_lines':
        # Plot current measure
        coords = action_pairs[('0', '0')]
        begin_coords = coords['Begin']
        end_coords = coords['End']

        if col == None and row == None:
            fig.add_trace(go.Scatter(
                x=[begin_coords[0], end_coords[0]],
                y=[begin_coords[1], end_coords[1]],
                mode='lines',
                line=dict(color=color if other_pathways else measure_colors.get('0', 'pink'), width=self.line_width_line, dash='dash' if other_pathways else 'solid'),
                showlegend=False,
                customdata=[key for key, array in measures_in_pathways.items()]
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[begin_coords[0], end_coords[0]],
                y=[begin_coords[1], end_coords[1]],
                mode='lines',
                line=dict(color=color if other_pathways else self.base_colors_sectors[risk_owner_hazard], width=self.line_width_line,
                          dash='dash' if other_pathways else 'solid'),
                showlegend=False,
                customdata=[key for key, array in measures_in_pathways.items()]
            ),
                row=row, col=col
            )


        for pathway, measures in measures_in_pathways.items():
            old_keys = []
            measures_split = [tuple(item.replace(']', '').split('[')) for item in measures]
            relevant_measures = {action_pairs[measure_instance]['Begin'][0]: measure_instance for measure_instance in measures_split if len(measure_instance) > 1}
            sorted_years = sorted(relevant_measures)

            # add lines based on increasing years
            for year in sorted_years:
                measure_instance = relevant_measures[year]
                coords = action_pairs[measure_instance]
                begin_coords = coords['Begin']
                end_coords = coords['End']
                measure, instance = measure_instance
                customdata = [key for key, array in measures_in_pathways.items() if f'{measure}[{instance}]' in array or (measure == '0' and f'{measure}' in array)]

                if col == None and row == None:
                    fig.add_trace(go.Scatter(
                        x=[begin_coords[0], end_coords[0]],
                        y=[begin_coords[1], end_coords[1]],
                        mode='lines',
                        line=dict(color=color if other_pathways else measure_colors.get(measure, 'pink'), width=self.line_width_line, dash='dash' if other_pathways else 'solid'),
                        showlegend=False,
                        customdata=customdata
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=[begin_coords[0], end_coords[0]],
                        y=[begin_coords[1], end_coords[1]],
                        mode='lines',
                        line=dict(color=color if other_pathways else self.base_colors_sectors[risk_owner_hazard],
                                  width=self.line_width_line, dash='solid'),
                        showlegend=False,
                        customdata=customdata
                    ), row=row, col=col)

                # if previous measures have not been replaced, plot a line for this as well between
                # given coordinates
                max_number_lines = len(old_keys)
                if max_number_lines == 1:
                    offset_lines = self.max_line_offset * .5
                else:
                    offset_lines = self.max_line_offset
                y_offsets1 = np.linspace(0, offset_lines, int(np.floor(max_number_lines * 2 / 2)) + 1)
                y_offsets2 = np.linspace(-offset_lines, 0, int(np.ceil(max_number_lines * 2 / 2)) + 1)[::-1]
                # Initialize the rearranged list
                rearranged_offsets = []

                # Interleave the values from y_offsets1 and y_offsets2
                for i in range(1, len(y_offsets2)):
                    rearranged_offsets.append(y_offsets1[i])
                    rearranged_offsets.append(y_offsets2[i])
                # Insert the zero value at the beginning
                rearranged_offsets.insert(0, 0.0)

                for i, previous in enumerate(old_keys):
                    if previous not in replacing_measure.get(measure, []):
                        ybegin_coords = begin_coords[1] + rearranged_offsets[i+1]
                        yend_coords = end_coords[1] + rearranged_offsets[i+1]
                        if col == None and row == None:
                            fig.add_trace(go.Scatter(
                                x=[begin_coords[0], end_coords[0]],
                                y=[ybegin_coords, yend_coords],
                                mode='lines',
                                line=dict(color=color if other_pathways else measure_colors.get(previous, 'pink'), width=self.line_width_line, dash='dash' if other_pathways else 'solid'),
                                showlegend=False,
                                customdata=customdata,
                                hovertext=customdata
                            ))
                        else:
                            fig.add_trace(go.Scatter(
                                x=[begin_coords[0], end_coords[0]],
                                y=[ybegin_coords, yend_coords],
                                mode='lines',
                                line=dict(color=color if other_pathways else self.base_colors_sectors[risk_owner_hazard],
                                          width=self.line_width_line, dash='solid'),
                                showlegend=False,
                                customdata=customdata,
                                hovertext=customdata
                            ), row=row, col=col)
                old_keys.append(measure)
    else:
        for (measure, instance), coords in action_pairs.items():
            customdata = [key for key, array in measures_in_pathways.items() if f'{measure}[{instance}]' in array or (measure == '0' and f'{measure}' in array)]
            if 'Begin' in coords and 'End' in coords:
                begin_coords = coords['Begin']
                end_coords = coords['End']
                if col == None and row == None:
                    fig.add_trace(go.Scatter(
                        x=[begin_coords[0], end_coords[0]],
                        y=[begin_coords[1], end_coords[1]],
                        mode='lines',
                        line=dict(color=color if other_pathways else measure_colors.get(measure, 'pink'), width=self.line_width_line, dash='dash' if other_pathways else 'solid'),
                        showlegend=False,
                        customdata=customdata,
                        hovertext=customdata
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=[begin_coords[0], end_coords[0]],
                        y=[begin_coords[1], end_coords[1]],
                        mode='lines',
                        line=dict(color=color if other_pathways else self.base_colors_sectors[risk_owner_hazard],
                                  width=self.line_width_line, dash='solid'),
                        showlegend=False,
                        customdata=customdata,
                        hovertext=customdata
                    ), row=row, col=col)
    return fig

def add_vertical_lines(self, fig, action_transitions, action_pairs, measures_in_pathways, offsets, line_width_line, measure_colors, risk_owner_hazard, color='grey',  other_pathways=False, row=None, col=None):
    """
    Adds vertical lines to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add lines to.
    - action_transitions: List of transitions between actions.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - measures_in_pathways: Dict of measures in each pathway.
    - offsets: Dict of offsets for measures.
    - line_width_line: Width of the lines.
    - measure_colors: Dict mapping measures to their colors.
    - other_pathways: Boolean indicating whether the lines belong to other pathways (colored grey).

    Returns:
    - fig: The Plotly figure with added vertical lines.
    """
    for transition in action_transitions:
        if isinstance(transition[2], int):
            # Skip horizontal lines
            continue
        else:
            start_measure, start_instance = find_first_and_second_integers(transition[0])
            end_measure, end_instance = find_first_and_second_integers(transition[2])
            end_x_pos = transition[1]

            customdata = [key for key, array in measures_in_pathways.items() if f'{end_measure}[{end_instance}]' in array or (end_measure == '0' and f'{end_measure}' in array)]

            if start_measure != '0':
                group_offset = offsets.get(start_measure, 0)
                end_x_pos += group_offset

            if (start_measure, start_instance) in action_pairs:
                if 'Begin' in action_pairs[(start_measure, start_instance)]:
                    start_y_pos = action_pairs[(start_measure, start_instance)]['Begin'][1]
                    end_y_pos = action_pairs[(end_measure, end_instance)]['End'][1]

                    if col == None and row == None:
                        fig.add_trace(go.Scatter(
                            x=[end_x_pos, end_x_pos],
                            y=[start_y_pos, end_y_pos],
                            mode='lines',
                            line=dict(color=color if other_pathways else measure_colors.get(start_measure, 'pink'), width=line_width_line, dash='dash' if other_pathways else 'solid'),
                            showlegend=False,
                            customdata=customdata,
                            hovertext=customdata
                        ))
                    else:
                        fig.add_trace(go.Scatter(
                            x=[end_x_pos, end_x_pos],
                            y=[start_y_pos, end_y_pos],
                            mode='lines',
                            line=dict(color=color if other_pathways else self.base_colors_sectors[risk_owner_hazard],
                                      width=line_width_line, dash='solid'),
                            showlegend=False,
                            customdata=customdata,
                            hovertext=customdata
                        ), row=row, col=col)
    return fig

def add_measure_buttons_plotly(self, fig, preferred_dict_inv, planning_horizon, risk_owner_hazard, col=None, row=None):
    """
    Adds measure buttons (logos) to the Plotly figure.

    Parameters:
    - fig: The Plotly figure to add buttons to.
    - preferred_dict_inv: Dict for measure button mappings.

    Returns:
    - fig: The Plotly figure with added measure buttons.
    """
    count_axis = len([x for x in fig.layout if x.startswith('xaxis')])

    for key, element in preferred_dict_inv.items():

        if col == None and row == None:
            img_path = f'data/logos/{risk_owner_hazard}/colorized/{self.inverted_measure_numbers[int(preferred_dict_inv[key])]}.png'
            base64_image = image_to_base64(img_path)
            fig.add_layout_image(
                dict(
                    source=base64_image,
                    xref="paper",  # Use "paper" for relative positioning
                    yref="y",  # Use axis ID for aligning with specific ticks
                    x=0,  # Adjust this value to position the image on the x-axis
                    y=key,  # Align with a specific y-axis tick label
                    sizex=0.7,
                    sizey=0.7,
                    xanchor="left",
                    yanchor="middle",
                ),
            )
        else:
            img_path = f'data/logos/{risk_owner_hazard}/{risk_owner_hazard}/uniform_color/{self.inverted_measure_numbers[int(preferred_dict_inv[key])]}.png'
            base64_image = image_to_base64(img_path)
            if col == row:
                if col == 1:
                    ref = 1
                else:
                    ref = col + row
            if col > row:
                ref = col
            if col < row:
                if count_axis == 4:
                    ref = row + col
                else:
                    ref = row
            fig.add_layout_image(
                dict(
                    source=base64_image,
                    xref=f"x{ref}",  # Use "paper" for relative positioning
                    yref=f"y{ref}",  # Use axis ID for aligning with specific ticks
                    x=planning_horizon[0],  # Adjust this value to position the image on the x-axis
                    y=key,  # Align with a specific y-axis tick label
                    sizex=5,
                    sizey=0.7,
                    xanchor="left",
                    yanchor="middle",
                )
            )
    return fig
