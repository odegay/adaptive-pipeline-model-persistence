db_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "version": {
            "type": "string"
        },
        "pipeline_id": {
            "type": "string"
        },
        "status": {
            "type": "number",
        },
        "current_hidden_layers_ct": {
            "type": ["number", "null"]
        },
        "current_configuration": {
            "type": ["string", "null"]
        },
        "hidden_layers_configs": {
            "type": ["array", "null"],
            "items": {
                "hidden_layers_ct": {
                    "type": "number"
                },
                "is_completed": {
                    "type": "boolean"
                },
                "MAX_accuracy": {
                    "type": "number"
                },
                "configurations": {
                    "type": "array",
                    "items": {
                        "configuration": {
                            "type": "string"
                        },
                        "accuracy": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    },
    "required": ["version", "pipeline_id", "status"],
    "additionalProperties": False
}            

 