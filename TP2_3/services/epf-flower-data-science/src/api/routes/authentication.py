import os
import json
import opendatasets as od
from config import kaggle


def _get_kaggle_credentials():
    """
    Get the user's kaggle username and key


    Returns:
        KAGGLE_USERNAME
        KAGGLE_API_KEY
    """


    return kaggle['username'], kaggle['key']

print (_get_kaggle_credentials())

# # URL of the dataset
# url = "https://www.kaggle.com/datasets/muratkokludataset/acoustic-extinguisher-fire-dataset"

# # Main function
# if __name__ == "__main__":
#     # Configure Kaggle credentials
#     configure_kaggle_credentials()

#     # Download the dataset using opendatasets
#     try:
#         od.download(url)
#         print("Dataset downloaded successfully.")
#     except Exception as e:
#         print(f"Error downloading dataset: {e}")
