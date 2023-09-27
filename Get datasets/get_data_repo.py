"""
these python scripts downloaded data repositories from github or huggingface
the data repositories information read from datasets_source.csv
"""
import pandas as pd
import os
from urllib.parse import urlparse
import re
import git

datasets_source_path = os.path.abspath("Get datasets/datasets_source.csv")
test_run = False

sources = pd.read_csv(datasets_source_path, index_col="Unique").dropna(subset="Link_to_download")

# assign the local repositories directory.
sources["Local_repo_dir"] = [ os.path.join(os.path.abspath("Get datasets/data_repo"), dir_name) for dir_name in sources.index]

# make projects directory.
for repo_dir in sources["Local_repo_dir"]:
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        
# print the dataset need to manually download
cloneable_list = []
print(f'please manually download these dataset. :')
for source in sources.itertuples():
    git_cloneable = bool(re.search("huggingface.co|github.com", urlparse(source.Link_to_download).netloc))
    if not git_cloneable or os.listdir(source.Local_repo_dir):
        print(f' - {source.Name} from {source.Link_to_download} download to {source.Local_repo_dir}')
    else:
        cloneable_list.append(source)
print()

#clone the datasets repository.
for source in cloneable_list:
    print(f"Cloning {source.Name} to {source.Local_repo_dir}")
    if not test_run: 
        try:
            git.Repo.clone_from(source.Link_to_download, to_path=source.Local_repo_dir)
        except Exception as e:
            print(f"An error occurred while cloning {source.Link_to_download}: {e}")        
        
print(f"cloned all datasets repositories")


