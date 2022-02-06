# time-profiler
Takes in an input of a path or a directory, It recursively finds out all the python files present in the directory and adds a decorator from a wrapper function. When an individual file is run, It logs the time taken for individual functions to run in the exec.log file which will be created within the directory.

To run:
path
|_____directory
      |__________path

$python time_profiler.py /path/directory
$python filename.py
