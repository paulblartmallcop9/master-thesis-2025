# Master Thesis
A Dutch LLM Benchmark: Benchmarking large language models on language understanding using language-specific linguistic puzzles by Maurice Voors

## Data Pipeline

The entire data pipeline can be run using `pipeline/run_pipeline.py` for collection, processing, annotation and preparation of the data. Manual annotation can be performed intermediate which is indicated when running the pipeline.

### Usage

To execute the full pipeline, run:

```bash
python3 pipeline/run_pipeline.py
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

### Scripts

Each step in the pipeline corresponds to a Python script. The scripts save the data intermediate and each step uses the output of the previous script.

| Script               | Output                            | Description                                  |
| -------------------- | ------------------------------- | -------------------------------------------- |
| `get_pages.py`       | `all_pages.txt`                 | Get disambiguation pages titles          |
| `get_contents.py`    | `all_content.txt`               | Get disambiguation pages HTML content        |
| `get_links.py`       | `all_links.txt`                 | Get related pages links from HTML content    |
| `filter1.py`         | `all_filtered1.txt`             | Filter disambiguation pages on disambiguation page titles   |
| `get_aspects.py`     | `all_aspects.txt`               | Get aspects from related pages           |
| `filter2.py`         | `all_filtered2.txt`             | Filter disambiguation pages on related page aspects |
| `annotations_out.py` | `all_annotations_out.tsv`       | Export data to file for annotation           |
| `annotations_in.py`  | `all_annotations_in.txt`        | Import annotation file with selected clues   |
| `create_puzzles.py`  | `test_puzzles.txt`, `dev_puzzles.txt`, … | Create puzzles                    |

To execute any script standalone, run:

```bash
python3 pipeline/<script_name.py>
```

## Experiments

The repository includes three Jupyter notebooks for running experiments with different model providers. Each notebook allows you to manually select model and shot configuration denoted via in-line comments.

| Notebook                       | Description                          | Requirements                      | 
| ------------------------------ | ------------------------------------ | --------------------------------- | 
| `experiment_api.ipynb`         | Experiments via API           | API key                    | 
| `experiment_huggingface.ipynb` | Experiments via Hugging Face         |  | 
| `experiment_ollama.ipynb`      | Experiments via Ollama | Pull desired Ollama model |

### Models

* **API** (large-scale multilingual): GPT-4o, LLama 3.3
* **Ollama** (small-scale multilingual): Gemma 3, Mistral, Llama 3.2
* **Hugging Face** (small-scale Dutch-specific): Fietje 2, Geitje Ultra

### Usage

1. Open the chosen Jupyter Notebook file.
2. Configure your environment:

   * **API notebook:** Set your `OPENAI_API_KEY` before running cells.
   * **Ollama notebook:** Run `ollama pull <model_name>` to download models locally.
3. Set the desired source file to import data to use in the experiment.
4. In each notebook, locate the `# set model` and `# set shot category` comments to manually input your model and shot type (zero-, one-, or three-shot using the predefined functions).
5. Execute cells sequentially and review results.

## Evaluation

The data can be evaluated using the `human_evaluation.py` file for the human evaluation and the `order_evaluation.py` file for the order evaluation.

### Human evaluation
Compare human annotation or agreement data against model predictions and categorize instances into:
 - Both correct
 - Model correct only
 - Human correct only
 - Both incorrect

#### Usage
To execute the human evaluation, run:

```bash
python3 evaluation/human_evaluation.py
```
Make sure to configure the file for the human data and the file for the model data.

        

### Order evaluation
Evaluate model performance across multiple experiment permutations and report:
 -  Number of correct instances and accuracy per file  
  -   Best permutation and its accuracy 
  -   Average accuracy across all permutations  
  -   Total and overlap accuracy

#### Usage
To execute the order evaluation, run:

```bash
python3 evaluation/order_evaluation.py
```
Make sure to configure the file for the model data by editing the file name to include the desired model to evaluate.
