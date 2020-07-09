import string
import json
from genson import SchemaBuilder
from pyresttest import validators

def json_schema_generator(config):
    """Creates a dummy validator that generates json schema for api call.
    This validator always fails.

    :config: Dictionary containing 'schema_file' and 'output_file' keys.
    Both are templated file names. Api call result will be saved to 'output_file', and generated schema in 'schema_file'.
    {schema_file: '$api/$method.json.schema', output_file: '$api/$method.json.out'}

    """
    output = JSONSchemaGenerator()
    output.schema_file = config['schema_file']
    output.output_file = config['output_file']
    return output

def gen_schema(json):
    """Returns schema for given json string

    :json: json string
    :returns: schema for given json

    """
    builder = SchemaBuilder()
    builder.add_object(json)
    return builder.to_json(indent=2)

def write(file_name, data):
    """Writes given data to file named filename

    :file_name: name of the output file
    :data: string to write

    """
    with open(file_name, "w") as f:
        f.write(data)

class JSONSchemaGenerator(validators.AbstractValidator):
    """ Does extract response body and compare with given my_file_name.json.pat.
        If comparison failed response is save into my_file_name.json.out file.
    """

    def validate(self, body=None, headers=None, context=None):
        extractor = validators._get_extractor({'jsonpath_mini': '.'})
        output = extractor.extract(body=body, headers=headers, context=context)
        schema_file = string.Template(self.schema_file).safe_substitute(context.get_values())
        output_file = string.Template(self.output_file).safe_substitute(context.get_values())
        write(output_file, json.dumps(output, indent=2))
        schema = gen_schema(output)
        write(schema_file, schema)
        return False

VALIDATORS = { 'json_schema_generate': json_schema_generator }
