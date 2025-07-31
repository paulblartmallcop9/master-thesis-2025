# Master Thesis
A Dutch LLM Benchmark: Benchmarking large language models on language understanding using language-specific linguistic puzzles

## Data Pipeline

The entire data pipeline can be run using `run_pipeline.py` for collection, processing, annotation and preparation of the data. Manual annotation can be performed intermediate which is indicated when running the pipeline.

### Usage

To execute the full pipeline, run:

```bash
python3 run_pipeline.py
```

On execution, the script will:

1. Run the initial preprocessing steps:

   * `get_pages.py` (Getting pages)
   * `get_contents.py` (Getting content)
   * `get_links.py` (Getting links)
   * `filter1.py` (Filtering pages)
   * `get_aspects.py` (Getting aspects)
   * `filter2.py` (Filtering aspects)
   * `annotations_out.py` (Export annotations file)

2. Prompt you to perform manual annotations.

3. After you complete and save annotations, the pipeline continues with post-annotation steps:

   * `annotations_in.py` (Import annotations file)
   * `create_puzzles.py` (Creating puzzles)

If you only need to run the steps after annotation, start the script with the `y` option. The script will then directly execute the post-annotation steps.

### Individual Scripts

Each step in the pipeline corresponds to a Python script that saves the data intermediate and can also be run on its own:

| Script               | Description                  |
| -------------------- | ---------------------------- |
| `get_pages.py`       | Getting disambiguation pages titles |
| `get_contents.py`  | Get disambiguation pages HTML content                         |
| `get_links.py`       | Get related pages links from HTML content                    |
| `filter1.py`         | Filtering disambiguation pages on disambiguation page titles              |
| `get_aspects.py`     | Getting aspects from related pages             |
| `filter2.py`         | Filtering disambiguation pages on related page aspects            |
| `annotations_out.py` | Export data to file for annotation      |
| `annotations_in.py`  | Import annotation file with selected clues      |
| `create_puzzles.py`  | Creating puzzles             |

Run any script standalone using:

```bash
python3 <script_name.py>
```
