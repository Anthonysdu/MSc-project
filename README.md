# msc-project
jbmc folder contains the wrapper script of JBMC for sv-comp, and witness validation tool for java. 
https://sv-comp.sosy-lab.org/2021/systems.php


What's new:

jbmc/Wit4JBMC.py: witness validation script for java.It takes a witness file and java files as input.
Run it with the command:

./Wit4JBMC.py --witness witness.GraphML ../sv-benchmarks/java/java-ranger-regression/alarm/impl/*.java

or

./Wit4JBMC.py --witness witness.GraphML ../sv-benchmarks/java/java-ranger-regression/alarm/impl


WitForJBMC.py defines the witness validation tool for BenchExec, should be copied into the tool directory: https://github.com/sosy-lab/benchexec/tree/master/benchexec/tools and reinstall BenchExec

How to run it in BenchExec:

cd jbmc

chmod +x Wit4JBMC.py

benchexec ../Tasks_JBMCWitnessValidator.xml --no-compress-results


