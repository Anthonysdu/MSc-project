#!/usr/bin/env python3
import sys
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from fnmatch import fnmatch
#Add the path of networkx to run benchexec. Should 'pip install networkx' first
sys.path.append('/home/tong/.local/lib/python3.8/site-packages')
from networkx import networkx as nx
#exit(0)

try:
 #missing witness or java files
 if len(sys.argv) <= 3:
  exit(1)
 else:
  TaskFile = ''
  benchmarks_dir = []
  for i in sys.argv:
   if '.java' in i:
    benchmarks_dir.append(i)  

   else:
    for i in sys.argv[3:]:
     for path, subdirs, files in os.walk(i):
      for name in files:
       if fnmatch(name, '*.java'):
        benchmarks_dir.append(os.path.join(path, name))
    break

  witness_File_Dir = sys.argv[2]
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
   fullfile = ''
   mainpath = ''
   verifier = ''
   verifierpath = ''
   for benchmark in benchmarks_dir:

    #print('qweqe' + benchmark[benchmark.rfind('/')+1:benchmark.find('.java')])
    type = []
    linenum = []
    counterexample = []
    witnessline = []
    detvars = []
    #print(benchmark)
   #exit(0)
    #benchmark = TaskFile + '/' + benchmark
    
    with open(benchmark,'r') as fi:
     for num,line in enumerate(fi,1):
      index = line.find ('Verifier.')
      index2 = line.find('Random()')
      if(index != -1):
       #type.append(line[index + 15:-4].lower().replace( ')','').replace('(',''))
       linenum.append(num)
      
      if(index2 != -1):
       #type.append(line[index2 + 15:-4].lower().replace( ')','').replace('(',''))
       linenum.append(num)
    for data in witnessFile.edges(data = True):
     if(data[2]['originFileName'] in benchmark and 'assumption.scope' in data[2]):
      scope = data [2]['assumption.scope']
      startLine = data[2]['startline']
      if benchmark[benchmark.rfind('/')+1:benchmark.find('.java')] in scope and startLine in linenum:
       str = data [2]['assumption']
       counterexample.append(str)
       witnessline.append(startLine)
    #exit(0)
    #print(counterexample)
    with open(benchmark,'r') as fi:
     for position,lineb in enumerate(fi,1):
      if position in witnessline:
       type.append(lineb.strip()[:lineb.strip().find('=')])
    #print(benchmark[:benchmark.find('.java')])
    witnessline = list(dict.fromkeys(witnessline))
    counterexample = list(dict.fromkeys(counterexample))
    
    if 'string' not in type:
     for type1,counterexample1,linenum1 in zip(type,counterexample,witnessline):
      detvars.append(type1 + ' ' + counterexample1[counterexample1.find('='):])
     #print(detvars)
     with open(benchmark,'rt') as ben:
      dir = benchmark[:benchmark.rindex('/')]
      if dir.strip().find('../') == 0:
       path = 'temp/' + dir.strip()[dir.strip().find('../')+3:]
      elif dir.strip().find('./') == 0:
       path = 'temp/' + dir.strip()[dir.strip().find('./')+2:]
      elif dir.strip().find('/') == 0:
       path = 'temp/' + dir.strip()[dir.strip().find('/')+1:]

      else:
       path = 'temp/' + dir.strip()
      #print(benchmark[:benchmark.rindex('/')])
      #path = 'init/'+ benchmark[:benchmark.rindex('/')]
      if not os.path.exists(path):
       os.makedirs(path)
      filename = benchmark[benchmark.rindex('/')+1:]

 
      if filename == 'Verifier.java':
       verifier = path
      if filename == 'Main.java':
       mainpath = path
      fullfile = path+'/'+filename + ' ' + fullfile
      with open(os.path.join(path, filename),'wt') as jsl:
       for line_num,line_ben in enumerate(ben):
        #print(line_num+1)
        #print(line_ben)
        if len(witnessline) > 0:
         if line_num + 1 == witnessline[0]:
          t = line_ben.replace(line_ben[: line_ben.index(';')+1].strip(),detvars[0])
          detvars.remove(detvars[0])
          witnessline.remove(witnessline[0])
         else:
          t = line_ben
        else:
         t = line_ben

        if ' void ' in t and ' main' in t and 'public ' not in t:
         t = 'public ' + t 

        jsl.write(t)
   
   
   cmd = 'javac ' + fullfile
   subprocess.Popen(cmd,shell=True).wait()

   path1 = mainpath +'/org/sosy_lab'
   if not os.path.exists(path1):
    os.makedirs(path1)
    verifierpath = path1
    shutil.move(verifier,verifierpath)

   cmd1 = 'java -ea -cp '+ mainpath + ' Main'
   subprocess.Popen(cmd1,shell=True).wait()
  else:
   print('No violation')
except Exception as e:
 print(e)

exit(0)
