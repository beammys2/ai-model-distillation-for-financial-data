# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helper functions for managing NIM model deployments via Entity Store API.

This module provides utility functions to interact with the Entity Store API for:
- Creating and deleting model deployments
- Managing models in the Entity Store registry
- Listing active deployments
"""
from typing import Optional, Dict, List, Any
import requests
import time


def delete_model_deployment(ENTITY_STORE_URL: str, name: str, namespace: str = "meta") -> Optional[Dict[str, Any]]:
    """Delete a model deployment from the Entity Store.
    
    Stops a running model deployment instance.
    
    Args:
        ENTITY_STORE_URL (str): Base URL of the Entity Store service
        name (str): Name of the model deployment to delete
        namespace (str, optional): Namespace of the model. Defaults to "meta"
        
    Returns:
        dict: Response JSON if successful, None otherwise
        
    Example:
        >>> delete_model_deployment("http://localhost:8000", "llama-3.2-1b", "meta")
    """
    url = f"{ENTITY_STORE_URL}/v1/deployment/model-deployments/{namespace}/{name}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Successfully deleted deployment {namespace}/{name}")
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def delete_model_from_store(ENTITY_STORE_URL: str, name: str, namespace: str = "meta") -> Optional[Dict[str, Any]]:
    """Delete a model from the Entity Store registry.
    
    Removes a model from the Entity Store model registry. This does not stop
    running deployments - use delete_model_deployment() for that.
    
    Args:
        ENTITY_STORE_URL (str): Base URL of the Entity Store service
        name (str): Name of the model to delete from registry
        namespace (str, optional): Namespace of the model. Defaults to "meta"
        
    Returns:
        dict: Response JSON if successful, None otherwise
        
    Example:
        >>> delete_model_from_store("http://localhost:8000", "customized-llama", "dfwbp")
    """
    url = f"{ENTITY_STORE_URL}/v1/models/{namespace}/{name}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Successfully deleted model {namespace}/{name} from Entity Store")
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def list_model_deployments(ENTITY_STORE_URL: str) -> Optional[List[Dict[str, Any]]]:
    """List all active model deployments.
    
    Retrieves a list of all currently running model deployments from the Entity Store.
    
    Args:
        ENTITY_STORE_URL (str): Base URL of the Entity Store service
        
    Returns:
        list: List of deployment dictionaries if successful, None otherwise
        
    Example:
        >>> deployments = list_model_deployments("http://localhost:8000")
        >>> print(f"Found {len(deployments)} deployments")
    """
    url = f"{ENTITY_STORE_URL}/v1/deployment/model-deployments"
    headers = {"accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        deployments = response.json()
        print(f"Found {len(deployments)} deployment(s):\n")
        return deployments
    else:
        print(f"Error: {response.text}")
        return None

def list_all_deployments(ENTITY_STORE_URL: str) -> None:
    """List all deployments with their actual names and namespaces.
    
    Args:
        ENTITY_STORE_URL (str): Base URL of the Entity Store service
        
    Example:
        >>> list_all_deployments("http://nemo.test")
    """
    url = f"{ENTITY_STORE_URL}/v1/deployment/model-deployments"
    response = requests.get(url, headers={"accept": "application/json"})
    
    if response.status_code == 200:
        data = response.json()
        deployments = data.get("data", [])
        print(f"Found {len(deployments)} deployment(s):")
        for dep in deployments:
            print(f"  - {dep['namespace']}/{dep['name']}")
    else:
        print(f"Error: {response.text}")

def create_model_deployment(ENTITY_STORE_URL: str, name: str, namespace: str = "meta", payload: Optional[Dict[str, Any]] = None) -> None:
    """Create a new model deployment.
    
    Deploys a model instance using the Entity Store API. The payload should contain
    the deployment configuration including model specifications, resource requirements,
    and deployment parameters.
    
    Args:
        ENTITY_STORE_URL (str): Base URL of the Entity Store service
        name (str): Name for the new deployment
        namespace (str, optional): Namespace for the deployment. Defaults to "meta"
        payload (dict, optional): Deployment configuration payload
        
    Returns:
        None: Prints the status code and response JSON
        
    Example:
        >>> config = {
        ...     "name": "llama-3.2-1b",
        ...     "namespace": "meta",
        ...     "image": "nvcr.io/nim/meta/llama-3.2-1b-instruct",
        ...     "gpus": 1
        ... }
        >>> create_model_deployment("http://localhost:8000", "llama-3.2-1b", payload=config)
    """
    url = f"{ENTITY_STORE_URL}/v1/deployment/model-deployments"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully created deployment {name} in namespace {namespace}")
        return response.json()
    else:
        print(f"Error: {response.status_code} {response.text}")
        return None
