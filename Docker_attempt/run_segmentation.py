import os
import shutil
import subprocess
from tqdm import tqdm

def empty_directory(target_dir):
    for entry in os.listdir(target_dir):
        entry_path = os.path.join(target_dir, entry)
        if os.path.isfile(entry_path):
            os.remove(entry_path)

def perform_segmentation_on_folder(base_folder):
    all_dir = os.path.join(base_folder, "all")
    in_dir = os.path.join(base_folder, "input")
    out_dir = os.path.join(base_folder, "output")

    unique_ids = set()
    for filename in os.listdir(all_dir):
        split_name = filename.split("_")
        if len(split_name) > 1:
            unique_ids.add(split_name[1])
    sorted_ids = sorted(unique_ids)

    empty_directory(in_dir)

    progress_bar = tqdm(sorted_ids, desc=f"Segmenting: {os.path.basename(base_folder)}",
                        bar_format="{l_bar}%s{bar}%s{r_bar}" % ("\033[32m", "\033[0m"), ncols=80)

    for case_id in progress_bar:
        related_files = [fname for fname in os.listdir(all_dir) if case_id in fname]
        for fname in related_files:
            shutil.copy2(os.path.join(all_dir, fname), os.path.join(in_dir, fname))

        subprocess.run([
            "docker", "run", "--rm", "--gpus", "all",
            "-v", f"{in_dir}:/input",
            "-v", f"{out_dir}:/output",
            "rixez/brats21nnunet"
        ])

        empty_directory(in_dir)

def main():
    processed_folders = [
        r"/home/fylypo/WB/BraTs_2023_processed",
        r"/home/fylypo/WB/BraTs_Africa_processed"
    ]

    for folder in processed_folders:
        if not os.path.isdir(folder):
            print(f"Folder not found: {folder}")
            continue
        perform_segmentation_on_folder(folder)

if __name__ == "__main__":
    main()