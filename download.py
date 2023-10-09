import wandb
import credentials as cre
wandb.login(key=cre.wandb_key)
run = wandb.init()
artifact = run.use_artifact('dylanon/text-summarization-model/slices:latest', type='dataset')
artifact_dir = artifact.download(root="datasets")