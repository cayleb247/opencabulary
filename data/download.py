import kagglehub

# Download latest version
path = kagglehub.dataset_download("bwandowando/479k-english-words")

print("Path to dataset files:", path)