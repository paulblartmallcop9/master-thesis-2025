import csv
import json


def import_to_txt(input_tsv, output_txt):
    """
    Converts a TSV file (with an 'answer' column and multiple 'clueX' columns)
    back into a .txt file format where each line is a stringified dictionary.

    Args:
        input_tsv (str): Path to the TSV file, typically created using `export_to_tsv`.
        output_txt (str): Path to the output .txt file containing one dictionary per line.

    Output:
        A .txt file where each line is a JSON string with keys: 'answer', 'clue1', 'clue2', ..., 'clueN'.
        Empty cells in the TSV are ignored.
    """
    with open(input_tsv, "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="\t")
        headers = next(reader)

        clue_headers = [h for h in headers if h.startswith("description")]

        with open(output_txt, "w", encoding='utf-8') as out:
            for row in reader:
                if not row:  # skip empty rows
                    continue
                answer = row[0].strip()
                clues = [clue.strip() for clue in row[1:] if clue.strip() != ""]

                item = {"answer": answer}
                for i, clue in enumerate(clues):
                    item[f"clue{i+1}"] = clue
                out.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():

    # define in- and output
    infile = "data/all_annotations_out.tsv"
    outfile = 'data/all_annotations_in.txt'

    # Example usage
    import_to_txt(infile, outfile)

if __name__ == "__main__":
    main()
