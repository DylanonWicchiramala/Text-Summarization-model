"""
these python scripts downloaded data repositories from github or huggingface
the data repositories information read from datasets_source.csv
"""
import pandas as pd
import os
from urllib.parse import urlparse
import re
import git
from datasets import load_dataset
import json

def main():
    
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
    git_list = []
    huggingface_list = []
    print(f'please manually download these dataset. :')
    for source in sources.itertuples():
        is_git = bool(re.search("github.com", urlparse(source.Link_to_download).netloc))
        is_huggingface = bool(re.search("huggingface.co", urlparse(source.Link_to_download).netloc))
        
        if is_huggingface:
            huggingface_list.append(source)
        elif is_git:
            git_list.append(source)
        else:
            print(f' - {source.Name} from {source.Link_to_download} download to {source.Local_repo_dir}')
    print()


    #clone the datasets repository.
    for source in git_list:
        print(f"Cloning {source.Name} to {source.Local_repo_dir}")
        
        if not test_run: 
            try:
                git.Repo.clone_from(source.Link_to_download, to_path=source.Local_repo_dir)
                
            except Exception as e:
                print(f"An error occurred while cloning {source.Link_to_download}: {e}")    
                
                
    for source in huggingface_list:
        print(f"Download dataset {source.Name} to {source.Local_repo_dir}")
        
        if not test_run: 
            
            local_path = lambda dir : os.path.join(source.Local_repo_dir, str(dir)+".json")
            cache_dir = os.path.join(source.Local_repo_dir, "data")
            
            huggingface_dataset_name = "/".join(urlparse(source.Link_to_download).path.split('/')[2:])
            
            try:
                dataset = load_dataset(huggingface_dataset_name, data_dir=cache_dir, cache_dir=cache_dir)

                for segment in dataset.key():

                    with open(local_path(segment),'w') as f:
                        json.dump(dataset[segment].to_dict(), f)

            except Exception as e:
                print(f"An error occurred while downloading {source.Link_to_download}: {e}")    
        
    print(f"cloned all datasets repositories")



if __name__ == '__main__':
    main()
        
else:
    main()