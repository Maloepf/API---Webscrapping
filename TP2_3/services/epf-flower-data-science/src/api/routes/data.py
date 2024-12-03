from fastapi import APIRouter, HTTPException, status
from src.schemas.message import MessageResponse
from src.schemas.patch import DatasetUpdate
from src.schemas.post import PostDataset
import json
import os

router = APIRouter()

#path to get data
endpoint_all_datasets = "/dataset"
path_post = "/dataset/add"
path_patch = "/dataset/edit"

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))

CONFIG_DATASET_PATH = os.path.join(project_root, "src/config/model_parameters.json")

@router.get(endpoint_all_datasets, name="All datasets available", response_model=MessageResponse)

def _get_all_datasets_info() -> MessageResponse:
    """
    Get the datasets that are in the config file to display at the at user.
    The aim is so show all available datasets to the user

    Returns:
        MessageResponse: A message response containing either the config file information or an error message.
    """
    
    try:    #to load the JSON config file
        
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
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No datasets available in the configuration."
        )
    
    
    # Create a list of all dataset names (keys)
    all_datasets = list(dataset.keys())

    # Check if the list of datasets is empty
    if not all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No datasets found in the configuration."
        )

    # Return the dataset names
    return MessageResponse(message="All datasets", data=dataset)

@router.patch(path_patch + "/{dataset_name}", name="Edit dataset", response_model=MessageResponse)
def patch_dataset(dataset_name: str, update_data: DatasetUpdate) -> MessageResponse:
    """
    Edit the dataset based on the dataset_name parameter.
    The dataset_name is used to look up a key in the loaded JSON dataset.

    Args:
        dataset_name (str): The name of the dataset to be edited.
        update_data (DatasetUpdate): The new data to update the dataset with.

    Returns:
        MessageResponse: A message response confirming the update or an error message.
    """

    try:
        # Load the JSON dataset file
        with open(CONFIG_DATASET_PATH, 'r') as f:
            dataset = json.load(f)

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dataset configuration file not found."
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error decoding the dataset configuration file."
        )
    
    # Check if the dataset exists
    if dataset_name in dataset:
        # Update the dataset with the new data
        dataset[dataset_name].update(update_data)

        # Save the changes back to the file
        try:
            with open(CONFIG_DATASET_PATH, 'w') as f:
                json.dump(dataset, f, indent=4)
        except IOError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save the updated dataset configuration file."
            )

        return MessageResponse(
            message=f"Dataset '{dataset_name}' updated successfully.",
            data=dataset[dataset_name]
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{dataset_name}' not found in the configuration."
        )
    
@router.post("/dataset/add/{dataset_name}", name="Add dataset", response_model=MessageResponse)
def post_dataset(dataset_name: str, dataset_data: PostDataset) -> MessageResponse:
    """
    Add a new dataset to the configuration file.

    Args:
        dataset_name (str): The name of the dataset to be added (will be used as the key).
        dataset_data (PostDataset): The data for the dataset to be added (name and url).

    Returns:
        MessageResponse: A response confirming the addition or an error message.
    """
    try:
        # Load the existing dataset configuration file
        with open(CONFIG_DATASET_PATH, 'r') as f:
            dataset = json.load(f)

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dataset configuration file not found."
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error decoding the dataset configuration file."
        )
    
    # Check if the dataset already exists
    if dataset_name in dataset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dataset '{dataset_name}' already exists."
        )
    
    # Add the new dataset
    dataset[dataset_name] = {
        "name": dataset_data.name,
        "url": dataset_data.url
    }

    # Save the updated dataset back to the configuration file
    try:
        with open(CONFIG_DATASET_PATH, 'w') as f:
            json.dump(dataset, f, indent=4)
    except IOError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the updated dataset configuration file."
        )

    # Return a success response
    return MessageResponse(
        message=f"Dataset '{dataset_name}' added successfully.",
        data=dataset[dataset_name]
    )