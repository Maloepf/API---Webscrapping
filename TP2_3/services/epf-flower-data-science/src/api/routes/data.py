from fastapi import APIRouter, HTTPException, status
from src.schemas.message import MessageResponse
import json
import os

router = APIRouter()

#path to get data
path_get = "/dataset/get"

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))

CONFIG_DATASET_PATH = os.path.join(project_root, "src/config/model_parameters.json")


@router.get(path_get + "/{dataset_request}", name="Get dataset", response_model=MessageResponse)

def get_dataset(dataset_request: str) -> MessageResponse:
    """
    Get the dataset based on the dataset_request parameter.
    The dataset_request is used to look up a key in the loaded JSON dataset.

    Args:
        dataset_request (str): The name of the dataset to be retrieved.

    Returns:
        MessageResponse: A message response containing either the dataset or an error message.
    """
    
    
    try:    #to load the JSON dataset file
        
        with open(CONFIG_DATASET_PATH, 'r') as f:
            dataset = json.load(f)

    except FileNotFoundError:   #if the config file not exists
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dataset configuration file not found."
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error decoding the dataset configuration file."
        )
    
    if dataset_request in dataset:
        data = dataset[dataset_request]
        return MessageResponse(message=f"Dataset '{dataset_request}' found", data=data)
    #TODO retrieve the data set and display it 
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{dataset_request}' not found in the configuration."
        )
    
