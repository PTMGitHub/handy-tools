import random
import sys

def pair_names(names):
    random.shuffle(names)
    pairs = []
    for i in range(0, len(names), 2):
        if i + 1 < len(names):
            pairs.append((names[i], names[i+1]))
        else:
            pairs.append((names[i], None))  # For odd number of names, one will be left unpaired
    return pairs

def main():
    names_with_statuses = sys.argv[1:]
    names = [(name.split(',')[0].strip(), name.split(',')[1].strip()) for name in names_with_statuses]

    remote_names = [name for name, status in names if status.lower() == "remote"]
    office_names = [name for name, status in names if status.lower() == "office"]

    remote_pairs = pair_names(remote_names)
    office_pairs = pair_names(office_names)

    # Handling any remaining individuals
    remaining_remote = [pair[0] for pair in remote_pairs if pair[1] is None]
    remote_pairs = [pair for pair in remote_pairs if pair[1] is not None]

    remaining_office = [pair[0] for pair in office_pairs if pair[1] is None]
    office_pairs = [pair for pair in office_pairs if pair[1] is not None]

    if remaining_remote:
        if remote_pairs:
            # Add remaining remote to the last pair
            last_pair = remote_pairs.pop()
            remote_pairs.append((last_pair[0], last_pair[1], remaining_remote.pop()))
        else:
            # If no pairs, create a new group
            remote_pairs.append((remaining_remote.pop(), None))

    if remaining_office:
        if office_pairs:
            # Add remaining office to the last pair
            last_pair = office_pairs.pop()
            office_pairs.append((last_pair[0], last_pair[1], remaining_office.pop()))
        else:
            # If no pairs, create a new group
            office_pairs.append((remaining_office.pop(), None))

    # Displaying the final group
    print("Remote Pairs:")
    for pair in remote_pairs:
        print(pair)

    print("\nOffice Pairs:")
    for pair in office_pairs:
        print(pair)

if __name__ == "__main__":
    main()
