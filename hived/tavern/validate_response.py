class PatternDiffException(Exception):
  pass

class NoResultException(Exception):
  pass

def json_pretty_string(json_obj):
  from json import dumps
  return dumps(json_obj, sort_keys=True, indent=2)

def save_json(file_name, response_json):
  """ Save response to file """
  with open(file_name, 'w') as f:
    f.write(json_pretty_string(response_json))
    f.write("\n")

def save_raw(file_name, msg):
  """ Save lack of response to file """
  with open(file_name, 'w') as f:
    f.write(msg)

RESPONSE_FILE_EXT = ".out.json"
PATTERN_FILE_EXT = ".pat.json"
def load_pattern(name):
  """ Loads pattern from json file to python object """
  from json import load
  ret = {}
  with open(name, 'r') as f:
    ret = load(f)
  return ret

def remove_tag(data, tags_to_remove):
  if not isinstance(data, (dict, list)):
    return data
  if isinstance(data, list):
    return [remove_tag(v, tags_to_remove) for v in data]
  return {k: remove_tag(v, tags_to_remove) for k, v in data.items() if k not in tags_to_remove}

def compare_response_with_pattern(response, method=None, directory=None, ignore_tags=None, error_response=False):
  """ This method will compare response with pattern file """
  import os
  response_fname = directory + "/" + method + RESPONSE_FILE_EXT
  if os.path.exists(response_fname):
    os.remove(response_fname)

  response_json = response.json()
  if ignore_tags is not None:
    assert isinstance(ignore_tags, list), "ignore_tags should be list of tags"
    response_json = remove_tag(response_json, ignore_tags)
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  if error is not None and not error_response:
    msg = "Error detected in response: {}".format(error["message"])
    save_json(response_fname, response_json)
    raise PatternDiffException(msg)
  if error is None and error_response:
    msg = "Error expected but got result: {}".format(result)
    save_json(response_fname, response_json)
    raise PatternDiffException(msg)

  if error_response:
    result = error
  if result is None:
    msg = "Error detected in response: result is null, json object was expected"
    save_json(response_fname, response_json)
    raise PatternDiffException(msg)

  import deepdiff
  pattern = load_pattern(directory + "/" + method + PATTERN_FILE_EXT)
  if ignore_tags is not None:
    pattern = remove_tag(pattern, ignore_tags)
  pattern_resp_diff = deepdiff.DeepDiff(pattern, result)
  if pattern_resp_diff:
    save_json(response_fname, result)
    msg = "Differences detected between response and pattern."
    raise PatternDiffException(msg)

def has_valid_response(response, method=None, directory=None, error_response=False, response_fname=None):
  import os
  if not response_fname:
    response_fname = directory + "/" + method + RESPONSE_FILE_EXT

  if os.path.exists(response_fname):
    os.remove(response_fname)

  response_json = response.json()
  if error_response:
    correct_response = response_json.get("error", None)
  else:
    correct_response = response_json.get("result", None)


  if correct_response is None:
    save_json(response_fname, response_json)
    msg = "Error detected in response: result is null, json object was expected"
    raise NoResultException(msg)
  else:
    save_json(response_fname, correct_response)