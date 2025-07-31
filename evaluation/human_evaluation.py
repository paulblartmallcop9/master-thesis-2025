import ast
import pandas as pd


# Enter file for human performance
with open('data/human_agreement.txt', 'r', encoding='utf-8') as f:
    human_data = [ast.literal_eval(line) for line in f if line.strip()]

# Enter file for modelperformance
with open('data/best_model_performance.txt', 'r', encoding='utf-8') as f:
    model_data = [ast.literal_eval(line) for line in f if line.strip()]

model_dict = {entry['prompt']: entry for entry in model_data}

records = []
for h in human_data:
    prompt = h['prompt']
    expected = None
    predicted = ""
    model_correct = False

    if prompt in model_dict:
        m = model_dict[prompt]
        expected = m['answer'].lower()
        predicted = m['result'].lower()
        model_correct = expected in predicted
    else:
        print(f"Puzzle not found: {prompt}")

    human_label = h['correct'].lower()
    human_correct = human_label in ['agree', 'yes']

    if model_correct and human_correct:
        category = 'both_correct'
    elif model_correct and not human_correct:
        category = 'model_only_correct'
    elif not model_correct and human_correct:
        category = 'human_only_correct'
    else:
        category = 'both_wrong'

    records.append({
        'prompt': prompt,
        'model_correct': model_correct,
        'human_correct': human_correct,
        'category': category
    })

df = pd.DataFrame(records)

# Sumary with counts and percentages
summary_counts = df['category'].value_counts().rename('count')
summary_percents = (df['category'].value_counts(normalize=True) * 100).round(1).rename('percent')

summary = pd.concat([summary_counts, summary_percents], axis=1)
print("\nInstances per category with percentages:")
print(summary)
