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


from Code_for_GenerationEvaluation.SequenceGenerator import SequenceGenerator
from Code_for_GenerationEvaluation.SequenceEvaluator import SequenceEvaluator
from Code_for_GenerationEvaluation.SequenceFilter import SequenceFilter
from Code_for_GenerationEvaluation.PathwaysInputGenerator import PathwaysInputGenerator

evaluation_criteria = ['Costs', 'Co-Benefits'] # in Interface: adding a checkbox for each column added to specify whether evaluation criteria or performance?

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



# Create the generator object
generator = SequenceGenerator(action_characterization, N=100, m=3)

# Generate and filter sequences
filtered_sequences = generator.generate_filtered_sequences()
print(filtered_sequences)

evaluation_keys = ['effectiveness', 'Costs', 'Co-Benefits']

filtering_conditions = {
    'effectiveness': ('above', '+'),
    'Costs': ('between', [40,160]),
    'Co-Benefits': ('between', ['----', '++'])
}

# Create the evaluator object
evaluator = SequenceEvaluator(filtered_sequences, action_characterization, evaluation_keys)

# Evaluate all sequences
performance = evaluator.evaluate_all_sequences()

# Print the results
print('performance', performance)

# Create the filter object
sequence_filter = SequenceFilter(performance, filtering_conditions)

# Filter sequences
filtered_sequences = sequence_filter.filter_sequences()

# Print the results
print('filtered pathways',filtered_sequences)

# Create the input generator object
generator = PathwaysInputGenerator(filtered_sequences, action_characterization)

# Generate input files
input_files = generator.generate_input_files()

# Print the results
print(input_files)

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
plt.show()