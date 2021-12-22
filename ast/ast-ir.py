import os
import logging
import argparse
import json


def load_json(jsfile: str):
  json_data = None
  with open(jsfile, 'r') as f:
    json_data = json.load(f)

  return json_data

def extract_function(ast: dict, filter: list):
  root = ast
  functions = {}
  while True:
    if root