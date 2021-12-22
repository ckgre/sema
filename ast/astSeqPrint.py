import json

class ASTSeq:
  def __init__(self, ast_json_file) -> None:
    with open(ast_json_file, 'r') as f:
      self.ast = json.load(f)

  def dfs(self, root):
    for key in root:
      if type(root[key]) is dict:
        self.dfs(root[key])
      elif type(root[key]) is list:
        for item in root[key]:
          self.dfs(item)
      else:
        pass
    for key in root:
      if type(root[key]) is not dict and type(root[key]) is not list:
        print(f"{key}: {root[key]}")

def test():
  a = ASTSeq("../../test/simple-ast/test0-ast.json")
  a.dfs(a.ast)

if __name__ == "__main__":
  test()