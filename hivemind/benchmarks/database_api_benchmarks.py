from requests import post
from json import dumps

def list_comments_by(start, order):
  test_args = {
    "jsonrpc":"2.0", 
    "method":"database_api.list_comments", 
    "params" : {
      "start" : start,
      "limit" : 10,
      "order" : order
    },
    "id":1
  }
  data = dumps(test_args)
  response = post("http://127.0.0.1:8080", data=data)
  response_json = response.json()
  return response_json

def find_comments(comments):
  test_args = {
    "jsonrpc":"2.0", 
    "method":"database_api.find_comments", 
    "params" : {
      "comments" : comments
    },
    "id":1
  }
  data = dumps(test_args)
  response = post("http://127.0.0.1:8080", data=data)
  response_json = response.json()
  return response_json

def test_list_comments_by_permlink(benchmark):
  response_json = benchmark(list_comments_by, ["steemit", "firstpost"], "by_permlink")
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"

def test_list_comments_by_parent(benchmark):
  response_json = benchmark(list_comments_by, ["steemit", "firstpost", "", ""], "by_parent")
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"

def test_list_comments_by_root(benchmark):
  response_json = benchmark(list_comments_by, ["steemit", "firstpost", "", ""], "by_root")
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"

def test_list_comments_by_cashout_time(benchmark):
  response_json = benchmark(list_comments_by, ["2016-07-08", "", ""], "by_cashout_time")
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"

def test_list_comments_by_author_last_update(benchmark):
  response_json = benchmark(list_comments_by, ["", "2016-08-28 17:15:12", "", ""], "by_author_last_update")
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"

def test_list_comments_by_last_update(benchmark):
  response_json = benchmark(list_comments_by, ["", "2016-08-28 17:15:12", "", ""], "by_last_update")
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"

def test_find_comments(benchmark):
  response_json = benchmark(find_comments, [["steemit", "firstpost"]])
  error = response_json.get("error", None)
  result = response_json.get("result", None)

  assert error is None, "Error detected"
  assert result is not None, "No result in response"
