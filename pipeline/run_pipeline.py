#!/usr/bin/env python3
import subprocess
import sys
import time


STEP_DESCRIPTIONS = {
"get_pages.py": "Getting pages",
"get_contents.py": "Getting content",
"get_links.py": "Getting links",
"filter1.py": "Filtering pages",
"get_aspects.py": "Getting aspects",
"filter2.py": "Filtering aspects",
"annotations_out.py": "Export annotations file",
"annotations_in.py": "Import annotations file",
"create_puzzles.py": "Creating puzzles",
}

def run_script(script, step=None, total=None):
    description = STEP_DESCRIPTIONS.get(script, script)
    prefix = f"[Step {step}/{total}] " if step and total else ""
    start_time = time.time()
    print(f"\n{prefix}{description} started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    elapsed = time.time() - start_time
    if result.returncode != 0:
        print(f"Error during {description}: return code {result.returncode}")
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)
    print(result.stdout)
    print(f"{prefix}{description} completed in {elapsed:.2f} seconds at {time.strftime('%Y-%m-%d %H:%M:%S')}")


def run_initial():
    initial_scripts = [
        #"get_pages.py",
        #"get_contents.py",
        #"get_links.py",
        #"filter1.py",
        "get_aspects.py",
        "filter2.py",
        "annotations_out.py",
    ]
    total = len(initial_scripts)
    print("\n=== Starting full pipeline run ===")
    for idx, script in enumerate(initial_scripts, start=1):
        run_script(script, step=idx, total=total)
    input("\nPlease perform annotations now and save the output. Exit or press Enter to continue...\n")


def run_post_annotations():
    post_scripts = [
        "annotations_in.py",
        "create_puzzles.py",
    ]
    total = len(post_scripts)
    print("\n--- Starting post-annotation steps ---")
    for idx, script in enumerate(post_scripts, start=1):
        run_script(script, step=idx, total=total)
    print("\n--- Post-annotation scripts complete ---")


def main():

    print(f"Experiment Runner initiated at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    first_choice = input("Run only post-annotation scripts? (y/N): ").strip().lower()
    if first_choice == 'y':
        run_post_annotations()
    else:
        run_initial()
        run_post_annotations()

if __name__ == "__main__":
    main()
