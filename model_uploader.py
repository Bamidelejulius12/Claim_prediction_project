from huggingface_hub import login, upload_folder

# (optional) Login with your Hugging Face credentials
login()

# Push your model files
upload_folder(folder_path="C:/Users/HP/Desktop/FNOL Project/models", repo_id="Julius911/FNOL_Model", repo_type="model")
