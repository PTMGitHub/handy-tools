import random
import sys
from graphviz import Digraph


def pair_names(names):
    random.shuffle(names)
    pairs = []
    i = 0
    while i < len(names):
        if i + 1 < len(names):
            pairs.append((names[i], names[i + 1]))
        else:
            pairs.append((names[i], None))  # For odd number of names, one will be left unpaired
        i += 2
    return pairs


def handle_odd_pairing(pairs):
    remaining = [pair[0] for pair in pairs if pair[1] is None]
    pairs = [pair for pair in pairs if pair[1] is not None]

    if remaining:
        if pairs:
            random_pair_index = random.randint(0, len(pairs) - 1)
            random_pair = pairs[random_pair_index]
            pairs[random_pair_index] = (random_pair[0], random_pair[1], remaining.pop())
        else:
            pairs.append((remaining.pop(), None, None))

    return pairs


def combine_pairs(pairs):
    combined = []
    while len(pairs) > 1:
        combined.append((pairs.pop(), pairs.pop()))
    if pairs:
        combined.append((pairs.pop(), None))  # In case of an odd number of pairs
    return combined


def handle_odd_combine_pairs(combine_pairs):
    remaining = [pair[0] for pair in combine_pairs if pair[1] is None]
    combine_pairs = [pair for pair in combine_pairs if pair[1] is not None]

    if remaining:
        if combine_pairs:
            random_pair_index = random.randint(0, len(combine_pairs) - 1)
            random_pair = combine_pairs[random_pair_index]
            combine_pairs[random_pair_index] = (random_pair[0], random_pair[1], remaining.pop())
        else:
            combine_pairs.append((remaining.pop(), None, None))

    return combine_pairs


def create_tree(pairs, combined_groups, label):
    dot = Digraph()
    dot.attr(rankdir="LR")

    for pair in pairs:
        pair_str = ' & '.join([name for name in pair if name])
        dot.node(pair_str, pair_str)
        for name in pair:
            if name:
                dot.edge(name, pair_str)

    for group in combined_groups:
        if group[1] is None:
            group_str = ' & '.join([name for name in group[0] if name])
        else:
            group_str = ' & '.join([' & '.join([name for name in pair if name]) for pair in group])
        dot.node(group_str, group_str)
        for pair in group:
            if pair:
                pair_str = ' & '.join([name for name in pair if name])
                dot.edge(pair_str, group_str)

    filename = f'tree_diagram_{label.lower()}'
    dot.render(filename, view=True)


def main():
    names_with_statuses = sys.argv[1:]
    names = [(name.split(',')[0].strip(), name.split(',')[1].strip()) for name in names_with_statuses]

    remote_names = [name for name, status in names if status.lower() == "remote"]
    office_names = [name for name, status in names if status.lower() == "office"]

    remote_pairs = pair_names(remote_names)
    office_pairs = pair_names(office_names)

    # Handle any remaining individuals by adding them to random pairs
    remote_pairs = handle_odd_pairing(remote_pairs)
    office_pairs = handle_odd_pairing(office_pairs)

    # Combine pairs into groups of four
    combined_remote_groups = combine_pairs(remote_pairs)
    combined_office_groups = combine_pairs(office_pairs)

    # Handle any remaining pair by adding them to random combined_pairs
    combined_remote_groups = handle_odd_combine_pairs(combined_remote_groups)
    combined_office_groups = handle_odd_combine_pairs(combined_office_groups)

    # Create the tree diagrams
    create_tree(remote_pairs, combined_remote_groups, "Remote")
    create_tree(office_pairs, combined_office_groups, "Office")


if __name__ == "__main__":
    main()
