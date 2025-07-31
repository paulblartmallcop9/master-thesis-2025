import ast
import csv


def export_to_tsv(input_file, output_tsv):
    """
    Converts a line-by-line text file with JSON-like dictionaries (containing 'title' and a list of 'links')
    into a tab-separated values (TSV) file for easy viewing/editing in spreadsheet applications.

    Each row will have the main title followed by the titles of each link.

    Args:
        input_file (str): Path to the input .txt file containing stringified dictionaries per line.
        output_tsv (str): Path to the output .tsv file to be created.
    """
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    rows = []
    max_links = 0

    for line in lines:
        # Parse each line into a dict
        data = ast.literal_eval(line)

        # Main title field
        title = data.get("title")
        if title is None:
            raise KeyError(f"Line missing 'title': {line}")

        # Extract list of links
        links = data.get("links", [])
        # Get the 'title' of each link
        link_titles = [link.get("title", "") for link in links]

        max_links = max(max_links, len(link_titles))
        # Build row: main title + all link titles
        rows.append([title] + link_titles)

    # Build headers: 'title' plus dynamic link columns
    headers = ["title"] + [f"description{i+1}" for i in range(max_links)]

    # Pad rows so every row has same number of columns
    for row in rows:
        if len(row) < len(headers):
            row.extend([""] * (len(headers) - len(row)))

    # Write out TSV
    with open(output_tsv, "w", newline='', encoding='utf-8') as out:
        writer = csv.writer(out, delimiter='\t')
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    infile = "data/all_filtered2.txt"
    outfile = "data/all_annotations_out.tsv"

    try:
        export_to_tsv(infile, outfile)
        print(f"Exported to TSV: {outfile}")
    except Exception as e:
        print(f"Error during export: {e}")


if __name__ == "__main__":
    main()
