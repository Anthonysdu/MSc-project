#!/usr/bin/env python3
import sys
import os
import subprocess
import xml.etree.ElementTree as ET
from shutil import copyfile

#Add the path of networkx to run benchexec. Should 'pip install networkx' first
sys.path.append('/home/tong/.local/lib/python3.8/site-packages')
from networkx import networkx as nx


#sys.argv[1] : '--witness'
#sys.argv[2] : witnessfile
#sys.argv[3...] :taskfiles
try:
 #missing witness or java files
 if len(sys.argv) <= 3:
  exit(1)
 else:
  #print('1111111')
  TaskFile = sys.argv[len(sys.argv)-1]
  witness_File_Dir = sys.argv[2].replace('*',TaskFile[TaskFile.rindex('/')+1:])
  #print(witnessFile)
  #print(TaskFile)
  try:
   witnessFile = nx.read_graphml(witness_File_Dir)
   violation = False
   for violationKey in witnessFile.nodes(data=True):
    if 'isViolationNode' in violationKey[1]:
     violation = True
  except Exception as e:
   violation = False
   exit(0)
  if(violation):
   type = ''
   linenum = []
   counterexample = ''
   for benchmark in os.listdir(TaskFile):
    benchmark = TaskFile + '/' + benchmark
  
   with open(benchmark,'r') as fi:
    for num,line in enumerate(fi,1):
     index = line.find ('Verifier.')
     if(index != -1):
      type = type + ' ' + line[index + 15:-4].lower().replace( ')','').replace('(','')
      linenum.append(num)

   for data in witnessFile.edges(data = True):
    if(data[2]['originFileName']==benchmark[benchmark.rfind('/')+1:] and 'assumption.scope' in data[2]):
     scope = data [2]['assumption.scope']
     startLine = data[2]['startline']
     if 'java::Main.main' in scope and startLine in linenum:
      str = data [2]['assumption']
      linenum.remove(startLine)
      counterexample = counterexample + '' + str[str.find('=')+1:str.find(';')]

   with open("ValidationHarnessTemplate.txt", "rt") as fin3:
    with open("ValidationHarness.java", "wt") as fout:
     for line3 in fin3:
      line3 = line3.replace('ClassName', 'Main')
      line3 = line3.replace('string_type', type)
      line3 = line3.replace('string_data', counterexample)
      fout.write(line3)

   copyfile(benchmark, benchmark[benchmark.rfind('/')+1:])
   p0 = subprocess.Popen(['javac', 'ValidationHarness.java'])
   p0.wait()
   p = subprocess.Popen(['java', '-ea', 'org.junit.runner.JUnitCore','ValidationHarness'])
   p.wait()
  else:
   print('No violation')
except Exception as e:
 print(e)

exit(0)
