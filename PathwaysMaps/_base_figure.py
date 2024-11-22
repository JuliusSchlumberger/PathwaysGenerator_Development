from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
from PathwaysMaps._find_integers import find_first_and_second_integers

def base_figure(self, data, action_pairs, action_transitions, offsets, preferred_dict_inv, measures_in_pathways, planning_horizon, ylabels):
    """
    Creates the base figure for the pathways map using Matplotlib.

    Parameters:
    - self: The class instance containing various configurations.
    - data: Dict containing plotting data organized by measure.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - action_transitions: List of transitions between actions.
    - offsets: Dict of offsets for measures.
    - preferred_dict_inv: Dict for measure button mappings.
    - measures_in_pathways: Dict of measures in each pathway.
    - ylabels: String whether to add logos, names or numbers to the plot.
    """

    # Add markers to the plot
    self.ax = add_actions(self.ax, data, self.line_width_marker, self.size_marker)

    # Add horizontal lines to the plot
    self.ax = add_horizontal_lines(self.ax, action_pairs, self.line_width_line, measures_in_pathways, self.line_choice, self.replacing_measure, self.measure_colors)

    # Add vertical lines to the plot
    self.ax = add_vertical_lines(self.ax, action_transitions, action_pairs, offsets, self.line_width_line, self.measure_colors)
    self.ax.set_xlim(planning_horizon)
    plt.xlabel('Years')
    plt.ylabel('Measures')
    plt.title('Base Pathways Map')

    if ylabels == 'logos':
        self.ax = add_logos(self.ax, preferred_dict_inv, self.measure_numbers_inv)
        self.ax.get_yaxis().set_visible(False)

    elif ylabels == 'names':
        # Retrieve and modify y-axis tick labels
        ytick_labels = self.ax.get_yticklabels()
        new_labels = []
        for ytick in ytick_labels:
            _, y_pos = ytick.get_position()
            ylabel = preferred_dict_inv.get(y_pos, None)

            if ylabel is None:
                new_labels.append('empty')
            elif ylabel == '0':
                new_labels.append('current')
            else:
                new_labels.append(self.measure_numbers_inv[int(ylabel)])

        self.ax.set_yticklabels(new_labels)
    else:
        # Retrieve and modify y-axis tick labels
        ytick_labels = self.ax.get_yticklabels()
        new_labels = []
        for ytick in ytick_labels:
            _, y_pos = ytick.get_position()
            ylabel = preferred_dict_inv.get(y_pos, None)

            if ylabel is None:
                new_labels.append('empty')
            elif ylabel == '0':
                new_labels.append('current')
            else:
                new_labels.append(ylabel)

        self.ax.set_yticklabels(new_labels)


    # Hide all spines except the bottom one
    for spine in ['top', 'right', 'left']:
        self.ax.spines[spine].set_visible(False)

    # Ensure the bottom spine is visible
    self.ax.spines['bottom'].set_visible(True)

def other_figure(self, data, action_pairs, action_transitions, offsets, preferred_dict_inv, measures_in_pathways, planning_horizon, ylabels, color='grey', alpha=0.8):
    """
    Creates the pathways map highlighting the effect of interactions using Matplotlib.

    Parameters:
    - self: The class instance containing various configurations.
    - data: Dict containing plotting data organized by measure.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - action_transitions: List of transitions between actions.
    - offsets: Dict of offsets for measures.
    - preferred_dict_inv: Dict for measure button mappings.
    - measures_in_pathways: Dict of measures in each pathway.
    - ylabels: String whether to add logos, names or numbers to the plot.
    """

    # Add markers to the plot
    self.ax = add_actions(self.ax, data, self.line_width_marker, self.size_marker, color, alpha, True)

    # Add horizontal lines to the plot
    self.ax = add_horizontal_lines(self.ax, action_pairs, self.line_width_line, measures_in_pathways, self.line_choice, self.replacing_measure, self.measure_colors, color, alpha, True)

    # Add vertical lines to the plot
    self.ax = add_vertical_lines(self.ax, action_transitions, action_pairs, offsets, self.line_width_line, self.measure_colors, color, alpha, True)

    self.ax.set_xlim(planning_horizon)
    plt.xlabel('Years')
    plt.ylabel('Measures')
    plt.title('Pathways Map: Effect of interactions')

def add_actions(ax, data, line_width_marker, size_marker, color='grey', alpha=0.8, other_pathways=False):
    """
    Adds action markers to the Matplotlib axis.

    Parameters:
    - ax: The Matplotlib axis to add markers to.
    - data: Dict containing plotting data organized by measure.
    - line_width_marker: Width of the marker lines.
    - size_marker: Size of the markers.
    - other_pathways: Boolean indicating whether the markers belong to other pathways (colored grey).

    Returns:
    - ax: The Matplotlib axis with added action markers.
    """
    zorder = 2 if other_pathways else 3

    for measure, points in data.items():
        for point in points:
            x, y = point[0]
            facecolor = color if other_pathways and point[3] != 'w' else point[3]
            edgecolor = color if other_pathways else point[2]

            ax.scatter(x, y, color=point[2], marker=point[1],
                       alpha=alpha if other_pathways else 1, edgecolors=edgecolor, facecolors=facecolor, linewidth=line_width_marker, s=size_marker, zorder=zorder)
    return ax

def add_horizontal_lines(ax, action_pairs, line_width_line, measures_in_pathways, line_choice, replacing_measure, measure_colors, color='grey', alpha=0.8, other_pathways=False):
    """
    Adds horizontal lines to the Matplotlib axis.

    Parameters:
    - ax: The Matplotlib axis to add lines to.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - line_width_line: Width of the lines.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - measures_in_pathways: Dict of measures in each pathway.
    - line_choice: Indicating whether different pathways are drawn with unique lines for active measures or just overlaid
    - replacing_measure: Dict of measures being replaced.
    - measure_colors: Dict mapping measures to their colors.
    - other_pathways: Boolean indicating whether the lines belong to other pathways (colored grey).

    Returns:
    - ax: The Matplotlib axis with added horizontal lines.
    """
    zorder = 1 if other_pathways else 1.5
    linestyle = '--' if other_pathways else '-'

    if line_choice == 'pathways_and_unique_lines':

        # Plot current measure
        coords = action_pairs[('0', '0')]

        begin_coords = coords['Begin']
        end_coords = coords['End']

        ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1], end_coords[1]], alpha=alpha if other_pathways else 1, color=color if other_pathways else measure_colors['0'], linewidth=line_width_line, linestyle=linestyle, zorder=zorder)


        for pathway, measures in measures_in_pathways.items():
            old_keys = []
            measures_split = [tuple(item.replace(']', '').split('[')) for item in measures]
            relevant_measures = {action_pairs[measure_instance]['Begin'][0]: measure_instance for measure_instance in measures_split if len(measure_instance) > 1}
            sorted_years = sorted(relevant_measures)

            for year in sorted_years:
                measure_instance = relevant_measures[year]
                coords = action_pairs[measure_instance]
                begin_coords = coords['Begin']
                end_coords = coords['End']
                measure, instance = measure_instance

                ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1], end_coords[1]], alpha=alpha if other_pathways else 1, color=color if other_pathways else measure_colors[measure], linewidth=line_width_line, linestyle=linestyle, zorder=zorder)

                for previous in old_keys:
                    if previous not in replacing_measure.get(measure, []):
                        ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1] - 0.04, end_coords[1] - 0.04], alpha=alpha if other_pathways else 1, color=color if other_pathways else measure_colors[previous], linewidth=line_width_line, linestyle=linestyle, zorder=zorder)

                old_keys.append(measure)
    else:
        for (measure, instance), coords in action_pairs.items():
            if 'Begin' in coords and 'End' in coords:
                begin_coords = coords['Begin']
                end_coords = coords['End']
                ax.plot([begin_coords[0], end_coords[0]], [begin_coords[1], end_coords[1]], alpha=alpha if other_pathways else 1, color=color if other_pathways else measure_colors[measure], linewidth=line_width_line, linestyle=linestyle, zorder=zorder)
    return ax

def add_vertical_lines(ax, action_transitions, action_pairs, offsets, line_width_line, measure_colors, color='grey', alpha=0.8, other_pathways=False):
    """
    Adds vertical lines to the Matplotlib axis.

    Parameters:
    - ax: The Matplotlib axis to add lines to.
    - action_transitions: List of transitions between actions.
    - action_pairs: Dict containing the start and end coordinates of actions.
    - offsets: Dict of offsets for measures.
    - line_width_line: Width of the lines.
    - measure_colors: Dict mapping measures to their colors.
    - other_pathways: Boolean indicating whether the lines belong to other pathways (colored grey).

    Returns:
    - ax: The Matplotlib axis with added vertical lines.
    """
    zorder = 1 if other_pathways else 1.5
    linestyle = '--' if other_pathways else '-'

    for transition in action_transitions:
        if isinstance(transition[2], int):
            # Skip horizontal lines
            continue
        else:
            start_measure, start_instance = find_first_and_second_integers(transition[0])
            end_measure, end_instance = find_first_and_second_integers(transition[2])
            end_x_pos = transition[1]

            if start_measure != '0':
                group_offset = offsets.get(start_measure, 0)
                end_x_pos += group_offset

            if (start_measure, start_instance) in action_pairs:
                if 'Begin' in action_pairs[(start_measure, start_instance)]:
                    start_y_pos = action_pairs[(start_measure, start_instance)]['Begin'][1]
                    end_y_pos = action_pairs[(end_measure, end_instance)]['End'][1]
                    ax.plot([end_x_pos, end_x_pos], [start_y_pos, end_y_pos], alpha=alpha if other_pathways else 1, color=color if other_pathways else measure_colors[start_measure], linewidth=line_width_line, linestyle=linestyle, zorder=zorder)
    return ax

def getImage(path):
    """
    Loads an image and returns an OffsetImage object.

    Parameters:
    - path: Path to the image file.

    Returns:
    - OffsetImage: The loaded image as an OffsetImage object.
    """
    return OffsetImage(plt.imread(path), zoom=0.03)

def add_logos(axes, preferred_dict_inv, measure_numbers_inv):
    """
    Adds logos to the Matplotlib axis based on measure positions.

    Parameters:
    - axes: The Matplotlib axis to add logos to.
    - preferred_dict_inv: Dict for measure button mappings.
    - measure_numbers_inv: Dict mapping measure numbers to their names.

    Returns:
    - axes: The Matplotlib axis with added logos.
    """
    ytick_labels = axes.get_yticklabels()

    for ytick in ytick_labels:
        _, y_pos = ytick.get_position()
        ylabel = preferred_dict_inv.get(y_pos, None)

        if ylabel == '0' or ylabel is None:
            continue

        # Add logo for the measure
        imagebox = getImage(f'data/logos/colorized/{measure_numbers_inv[int(ylabel)]}.png')
        ab = AnnotationBbox(imagebox, (0, y_pos), xybox=(0, 0), xycoords=("axes fraction", "data"), boxcoords="offset points", box_alignment=(0, .5), bboxprops={"edgecolor": "none"}, frameon=False)
        axes.add_artist(ab)

    return axes
