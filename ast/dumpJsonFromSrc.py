import argparse
import os
import logging
from subprocess import Popen, PIPE, DEVNULL
import argparse
import json
from collections import OrderedDict
import sys
sys.path.append('../../utils')
from utils.utils import create_new_dir, count_errors
from utils.mylogger import *

# 使用clang -Xclang 直接获得json格式的ast树

# EXTRA_ARG = ""
# OUT_DIR = ""

def is_json(myjson):
  try:
    # import pdb
    # pdb.set_trace()
    js = json.loads(myjson)
    if type(js) == type(json.loads("{}")):
      return True
    else:
      return False
  except ValueError:
    return False

def filter_json(dict_var: dict, filters: list, out: dict):
    # import pdb
    # pdb.set_trace()
    for k, v in dict_var.items():
        if type(v) is str:
            # st = v.encode('utf-8')
          if v in filters:
              out[v].append(dict_var)
              break
        elif type(v) is dict:
            filter_json(v, filters, out)
        elif type(v) is list:
            for e in v:
                if type(e) is dict:
                    filter_json(e, filters, out)

def dump_ast_json(params: tuple):
  path = params[0] # args[0]
  extra_arg = params[1] # args[1]
  out_dir = params[2] # args[2]
  _filters = set(params[3].strip().split(','))
  _cmd = ["clang", "-Xclang", "-ast-dump=json", path, extra_arg]
  logger.warning(wcolor.format(f"Dump AST of {path}"))
  # _out_dir = os.path.join(os.path.dirname(os.path.dirname(path)), "ast")
  _out = os.path.join(out_dir,
                      f"{os.path.splitext(os.path.basename(path))[0]}-ast.json")
  
  ret = 0
  with Popen(_cmd, stdout=PIPE, stderr=DEVNULL) as proc:
    logger.warning(wcolor.format(f"Save dump result to {_out}"))
    res = bytes.decode(proc.stdout.read())
    # debugger.error(ecolor.format(res))
    # debugger.warning(dcolor.format(f"is_json() = {is_json(res.strip())}"))
    try:
      _ast_json = json.loads(res.strip())
      if _filters == None:
        with open(_out, "w") as log:
          json.dump(_ast_json, log)
      else:
        _ast_filter_out = {}
        for _e in _filters:
          _ast_filter_out[_e] = []
        filter_json(_ast_json, _filters, _ast_filter_out)
        with open(_out, "w") as log:
          json.dump(_ast_filter_out, log)
      logger.warning(scolor.format(f"Successfully dump AST of {path} to .json {_out}"))
    except ValueError:
      errorer.error(ecolor.format(f"Error when dump AST of {path}"))
      ret = -1
  return ret

def batch_dump_ast(path: str, process: int, error_log: str, extra_arg: str, _filters: list):
  path = os.path.abspath(path)
  _files = [os.path.join(path, _f) for _f in os.listdir(path)]
  logger.warning(wcolor.format(f"Begin to process source code files in {path}"))
  _out_dir = os.path.join(os.path.dirname(path), 'ast')
  logger.warning(wcolor.format(f"Json files of ASTs will be save to {_out_dir}"))
  _out_dir = create_new_dir(_out_dir)

  # OUT_DIR = _out_dir
  logger.warning(wcolor.format(f"Creating output directory {_out_dir}"))
  os.makedirs(_out_dir)

  logger.warning(scolor.format("Begin dumping ASTs..."))
  _params = [(_f, extra_arg, _out_dir, _filters) for _f in _files]
  from multiprocessing import Pool
  with Pool(process) as p:
    p.map(dump_ast_json, _params)
  
  # for _p in _params:
  #   dump_ast_json(_p)

  err_cnt = count_errors(_files, os.listdir(_out_dir), error_log, "-ast.json")
  logger.warning(scolor.format(f"{len(_files)-err_cnt} of {len(_files)} are successfully dumped to .json files."))
  if err_cnt > 0:
    errorer.error(ecolor.format(f"{err_cnt} encounted errors when dump to json. Please read {error_log} to check them."))
  
  return len(_files) - err_cnt

def main():
  parser = argparse.ArgumentParser(add_help=True)
  parser.add_argument('-i', "--input", help="Path of source code files. dir", required=True)
  parser.add_argument('-p', "--process-num", help="Number of process to create.", required=False, default=8, type=int)
  parser.add_argument('-e', "--error-log", help="Output failed compiled files' list to this file.", required=False, default='error.log')
  parser.add_argument('--extra-args', help="Extra compiler options.", required=False, default="")
  parser.add_argument('--filters', help="comma separated list of AST filters. Ex: --filters=TypedefDecl,BuiltinType,main", default='', action="store", required=False)
  parser.add_argument('-v', '--version', action='version', help="Show program's version number and exit", version="%(prog)s 1.0")

  args = parser.parse_args()

  cnt = 0
  if not os.path.isdir(args.input):
    print("\033[31mINPUT option ERROR. Please input a directory.\n\033[0m")
    parser.print_help()
  else:
    # EXTRA_ARG = args.extra_args
    logger.warning(scolor.format(f"Use {args.process_num} processes"))
    logger.warning(wcolor.format(f"Will use the following filters: {args.filters}"))
    cnt = batch_dump_ast(args.input, args.process_num, args.error_log, args.extra_args, args.filters)
  
  return cnt

if __name__ == '__main__':
  exit(main())
