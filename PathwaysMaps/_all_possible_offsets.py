import itertools
import copy
import random

def all_possible_offsets(base_y_offset_dict, instance_dict, y_offsets, num_iterations):
    # Step 1: Initialize the candidate dict with base_y_offset_dict values
    optimized_dict = copy.deepcopy(base_y_offset_dict)

    # Step 2: Identify keys and instances that need offset assignment
    keys_to_optimize = {key: [] for key in instance_dict}
    for key in instance_dict:
        if key not in optimized_dict:
            optimized_dict[key] = {}
        for instance in instance_dict[key]:
            if optimized_dict[key].get(instance) is None:
                keys_to_optimize[key].append(instance)

    # Step 3: Generate all possible combinations of offsets for the undefined instances
    def generate_combinations(keys_to_optimize, y_offsets):
        all_combinations = []
        for key, instances in keys_to_optimize.items():
            num_instances = len(instances)

            # If len(instances) is not a round number and y_offsets is long enough, include one extra offset
            if num_instances % 2 != 0 and len(y_offsets) >= num_instances + 1:
                combs = list(itertools.permutations(y_offsets[:num_instances + 1], num_instances))
            else:
                # Generate all unique permutations of the required number of offsets
                combs = list(itertools.permutations(y_offsets[:num_instances], num_instances))

            if len(combs) > 12:  # If too many, randomly sample
                combs = random.sample(combs, 12)

            all_combinations.append((key, combs))
        return all_combinations

    # Step 4: Combine the combinations across all keys
    def combine_all_combinations(combination_sets, num_iterations):
        if not combination_sets:
            return [{}]  # If no combinations, return an empty dict

        key, combinations = combination_sets[0]
        rest_combinations = combine_all_combinations(combination_sets[1:], num_iterations)

        combined_results = []

        tick = 0
        for comb in combinations:
            for rest_comb in rest_combinations:
                combined_result = {key: dict(zip(keys_to_optimize[key], comb))}
                combined_result.update(rest_comb)
                combined_results.append(combined_result)
            tick += 1
            if isinstance(num_iterations, int):
                if tick > num_iterations:
                    break

        return combined_results

    # Step 5: Create all possible optimized_dict configurations
    # print(keys_to_optimize, y_offsets)
    combination_sets = generate_combinations(keys_to_optimize, y_offsets)
    all_combined_combinations = combine_all_combinations(combination_sets, num_iterations)

    # Step 6: Create all possible optimized dictionaries
    all_possible_dicts = []
    for comb_dict in all_combined_combinations:
        candidate_dict = copy.deepcopy(optimized_dict)
        for key, instance_values in comb_dict.items():
            candidate_dict[key].update(instance_values)
        all_possible_dicts.append(candidate_dict)

    return all_possible_dicts