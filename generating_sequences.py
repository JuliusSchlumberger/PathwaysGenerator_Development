from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import (
    action_level_by_first_occurrence,
    read_sequences,
    read_tipping_points,
    sequence_graph_to_pathway_map,
    sequences_to_sequence_graph,
)
from adaptation_pathways.plot import init_axes
from adaptation_pathways.plot import plot_classic_pathway_map as plot

from Code_for_GenerationEvaluation.generate_input_files import generate_input_files

action_characterization = {
    'Sea Wall': {
        'effectiveness': '++',
        'Costs': 90,
        'Co-Benefits': '-',
        'interactions_performance': [('replaces', 'Dike'), ('increase', 'effectiveness', 'Pump', 12)],
        'requirements_action': [('blocks', 'Salt Marshes')]
    },
    'Pump': {
        'effectiveness': '+',
        'Costs': 45,
        'Co-Benefits': '--',
        'interactions_performance': [],
        'requirements_action': [('after', ['Sea Wall'])]
    },
    'Dike': {
        'effectiveness': '++',
        'Costs': 60,
        'Co-Benefits': '0',
        'interactions_performance': [('replaces', 'Sea Wall'), ('decrease', 'effectiveness', 'Pump', '10%')],
        'requirements_action': [('before', 'Sea Wall')]
    },
    'Salt Marshes': {
        'effectiveness': '+',
        'Costs': 80,
        'Co-Benefits': '++',
        'interactions_performance': [('increases', 'effectiveness', 'Sea Wall', '10%', [0,2])],
    },
}

evaluation_keys = ['effectiveness', 'Costs', 'Co-Benefits']

filtering_conditions = {
    'effectiveness': ('above', '+'),
    'Costs': ('between', [40,160]),
    'Co-Benefits': ('between', ['----', '++'])
}

identifier = 'test'

generate_input_files(action_characterization, evaluation_keys, filtering_conditions,
                     f'data/pathways_generator/sequences_{identifier}.txt',
                     f'data/pathways_generator/xpositions_{identifier}.txt',
                     0,1000,3 )

pg_sequences = read_sequences('sequences.txt')
sequence_graph = sequences_to_sequence_graph(pg_sequences)
level_by_action = action_level_by_first_occurrence(pg_sequences)

pathway_map = sequence_graph_to_pathway_map(sequence_graph)
tipping_points = read_tipping_points('xpositions.txt', pathway_map.actions(),)

pathway_map.assign_tipping_points(tipping_points)
pathway_map.set_attribute("level", level_by_action)

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot(axes, pathway_map)
plt.savefig('pathways_map.png', dpi=300)
plt.show()