#!/usr/bin/env python3
import sys
import os
import subprocess
import xml.etree.ElementTree as ET

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
   type = []
   linenum = []
   counterexample = []
   detvars = []
   for benchmark in os.listdir(TaskFile):
    benchmark = TaskFile + '/' + benchmark
  
   with open(benchmark,'r') as fi:
    for num,line in enumerate(fi,1):
     index = line.find ('Verifier.')
     if(index != -1):
      type.append(line[index + 15:-4].lower().replace( ')','').replace('(',''))
      linenum.append(num)

   for data in witnessFile.edges(data = True):
    if(data[2]['originFileName']==benchmark[benchmark.rfind('/')+1:] and 'assumption.scope' in data[2]):
     scope = data [2]['assumption.scope']
     startLine = data[2]['startline']
     if 'java::Main.main' in scope and startLine in linenum:
      str = data [2]['assumption']
      counterexample.append(str)
   #print(type)
   #print(linenum)
   #print(counterexample)
   if 'string' not in type:
#   p = subprocess.Popen(['jshell', '-R','-ea'], stdin=subprocess.PIPE,stderr=subprocess.PIPE)
#    for type1,counterexample1,linenum1 in zip(type,counterexample,linenum):
#     detvars.append(type1 + ' ' + counterexample1)
#    with open(benchmark,'rt') as ben:
#     for line_num,line_ben in enumerate(ben):
#      if len(linenum) > 0:
#       if line_num + 1 == linenum[0]:
#        t = bytes(line_ben.replace(line_ben[: line_ben.index(';')+1].strip(),detvars[0]) + '\n','utf-8')
#        detvars.remove(detvars[0])
#        linenum.remove(linenum[0])
#       else:
#        t = bytes(line_ben, 'utf-8')
#      else:
#       t = bytes(line_ben, 'utf-8')
#      p.stdin.write(t)
#    p.stdin.write(bytes('Main.main(new String[0])\n','utf-8'))
#    p.stdin.write(bytes('/list\n','utf-8'))
#   p.stdin.write(bytes('/exit\n','utf-8'))
#   p.stdin.flush()
#   p.wait()
    for type1,counterexample1,linenum1 in zip(type,counterexample,linenum):
     detvars.append(type1 + ' ' + counterexample1)
    with open(benchmark,'rt') as ben:
     with open('Main.java','wt') as jsl:
      for line_num,line_ben in enumerate(ben):
       if len(linenum) > 0:
        if line_num + 1 == linenum[0]:
         t = line_ben.replace(line_ben[: line_ben.index(';')+1].strip(),detvars[0])
         detvars.remove(detvars[0])
         linenum.remove(linenum[0])
        else:
         t = line_ben
       else:
        t = line_ben
       jsl.write(t)
      #jsl.write('Main.main(new String[0])\n')
      #jsl.write('/list\n')
      #jsl.write('/exit\n')
    subprocess.Popen(['javac','Main.java']).wait()
    subprocess.Popen(['java','-ea','Main']).wait()
   else:
    print('failure')
  else:
   print('No violation')
except Exception as e:
 print(e)

exit(0)
