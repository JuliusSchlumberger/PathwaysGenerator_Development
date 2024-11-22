

def get_first_measures_for_offset(edge_list):
    y_offsets_at_zero = {'0': {'0': 0}}

    for edge in edge_list:
        if 'End(0[0]' in edge[0]:
            measure_instance_zero_offset = edge[2].split('ActionBegin(')[1].split('[')
            y_offsets_at_zero[measure_instance_zero_offset[0]] = {measure_instance_zero_offset[1][:-1]: 0 }
    return y_offsets_at_zero