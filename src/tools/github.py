def prepare_create_repo_payload(parameters):
    return {
        "action": "create_repository",
        "name": parameters["name"],
        "description": parameters.get("description", ""),
        "visibility": parameters.get("visibility", "public")
    }
