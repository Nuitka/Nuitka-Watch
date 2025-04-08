# nuitka-project: --mode=standalone

from jsonschema import ValidationError, validate

if __name__ == '__main__':
    schema = {
        "type": "object",
        "properties": {
            "price": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
        },
    }

    validate(instance={"name": "Eggs", "price": 34.99}, schema=schema)
    try:
        validate(
            instance={
                "name": "Eggs",
                "price": "Invalid"
            },
            schema=schema,
        )
    except ValidationError as e:
        print(e.message)
        print(e.absolute_path)
        print(e.absolute_schema_path)