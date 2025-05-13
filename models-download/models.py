from huggingface_hub import snapshot_download
import os

def download_all_models():
    print("Downloading bge-m3 model...")
    snapshot_download(
        repo_id="BAAI/bge-m3",
        local_dir="app/models/bge-m3",
        local_dir_use_symlinks=False
    )

    print("Downloading bge-reranker-large model...")
    snapshot_download(
        repo_id="BAAI/bge-reranker-large",
        local_dir="app/models/bge-reranker-large",
        local_dir_use_symlinks=False
    )

if __name__ == "__main__":
    os.makedirs("app/models", exist_ok=True)
    download_all_models()

