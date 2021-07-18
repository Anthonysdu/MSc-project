import benchexec.tools.template
import benchexec.result as result
import sys
import os, psutil
import subprocess
import networkx as nx
#import xml.etree.ElementTree as ET
import yaml
from shutil import copyfile
from bs4 import BeautifulSoup
import codecs
import time
from xml.etree import ElementTree

class Tool(benchexec.tools.template.BaseTool2):
 def executable(self, tool_locator):
  return tool_locator.find_executable("UBWitForJBMC.py")
 def name(self):
  return "UBWitForJBMC"
 def cmdline(self, executable, options, task, rlimits):
  return [executable] + options + list(task.input_files_or_identifier)
 def determine_result(self, run): 
  output = run.output
  validation = 'unknown'
  for line in output:
   if 'Exception java' in line or 'failure' in line or 'Java Exception' in line:
    validation = 'false'
    break
   else:
    validation = 'true'
  #exit_code = run.exit_code
  #status = 'False'
  if validation == 'false':
   status = result.RESULT_FALSE_PROP
  #print(exit_code)
  elif validation == 'true':
   status = result.RESULT_TRUE_PROP
  else:
   status = result.RESULT_UNKNOWN
  return status
