from Code_for_GenerationEvaluation.SequenceGenerator import SequenceGenerator
from Code_for_GenerationEvaluation.SequenceEvaluator import SequenceEvaluator
from Code_for_GenerationEvaluation.SequenceFilter import SequenceFilter
from Code_for_GenerationEvaluation.PathwaysInputGenerator import PathwaysInputGenerator

def generate_input_files(action_characterization, evaluation_keys, filter_conditions,sequence_file='sequences.txt', xposition_file='xpositions.txt', end_current_system=0, N=100, m=3):

    # Create the generator object
    generator = SequenceGenerator(action_characterization, N, m)

    # Generate and filter sequences
    filtered_sequences = generator.generate_filtered_sequences()

    # Create the evaluator object
    evaluator = SequenceEvaluator(filtered_sequences, action_characterization, evaluation_keys)

    # Evaluate all sequences
    performance = evaluator.evaluate_all_sequences()

    # Create the filter object
    sequence_filter = SequenceFilter(performance, filter_conditions)

    # Filter sequences
    filtered_sequences = sequence_filter.filter_sequences()

    # Create the input generator object
    generator = PathwaysInputGenerator(filtered_sequences, action_characterization)

    # Generate input files
    generator.generate_input_files(sequence_file, xposition_file, end_current_system)

