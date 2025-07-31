import ast
from collections import defaultdict

def load_data(file):
    """
    Read each line from a file as a Python dict.

    Args:
        file (str): Path to the file containing one dict per line.

    Returns:
        List[dict]: A list of dictionaries parsed from each line.
    """
    with open(file, 'r', encoding='utf-8') as f:
        return [ast.literal_eval(line.strip()) for line in f]


def compare_with_expected(data):
    """
    Compare predicted answers with expected answers for a list of entries.

    An entry is considered correct if its expected answer is a substring of the predicted answer,
    case-insensitive.

    Args:
        data (List[dict]): A list of prediction records, each containing 'expected' and predicted fields.

    Returns:
        Set[int]: A set of indices for which the predicted answer contains the expected answer.
    """
    correct_indices = set()
    for i, entry in enumerate(data):
        predicted = entry.get('result').lower()
        expected = entry.get('answer', '').lower()
        if expected and expected in predicted:
            correct_indices.add(i)
    return correct_indices


def main():

    all_data = {}
    correct_by_file = {}

    print("Loading data and evaluating...")

    # Load all six files
    for i in range(1, 7):
        fname = f'data/results_poss_{i}_gpt4o.txt'
        data = load_data(fname)
        all_data[f'file_{i}'] = data
        correct_by_file[f'file_{i}'] = compare_with_expected(data)

    # Calculate accuracies per run
    accuracies = {}
    for name, indices in correct_by_file.items():
        total = len(all_data[name])
        correct = len(indices)
        accuracies[name] = correct / total

    # Determine best and average accuracy
    best_name, best_acc = max(accuracies.items(), key=lambda x: x[1])
    avg_acc = sum(accuracies.values()) / len(accuracies)

    # Compute unique correct and full overlap
    all_correct_sets = list(correct_by_file.values())
    total_unique_correct = set.union(*all_correct_sets)
    total_overlap_all = set.intersection(*all_correct_sets)

    # Print results
    print("\nNumber of correct instances and accuracy per permutation:")
    for name, indices in correct_by_file.items():
        total = len(all_data[name])
        print(f"{name}: {len(indices)} / {total}    Accuracy: {accuracies[name]:.2%}")

    print(f"\nBest accuracy: {best_name} with {best_acc:.2%}")
    print(f"Average accuracy: {avg_acc:.2%}")

    print(f"\nTotal accuracy: {len(total_unique_correct)}")
    print(f"Overlap accuracy: {len(total_overlap_all)}")

if __name__ == "__main__":
    main()