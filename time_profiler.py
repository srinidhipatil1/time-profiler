from asyncore import read
from posixpath import basename
import time
import inspect
import os
from shutil import copyfile
from inspect import getmembers, isfunction
from sys import argv
import logging
import os, fnmatch

d = {}
def timeis(func):
    def wrap(*args, **kwargs):

        logging.basicConfig(filename = 'exec.log', level = logging.INFO, format= '%(message)s') #creates exec.log file

        l = open('exec.log','r') # adds the header if file is empty
        ls = l.readlines()
        if len(ls)==0:
            logging.info('path,method,time')
        l.close()

        start = time.time() #checks for time.
        result = func(*args, **kwargs)
        end = time.time()

        primary_key = str(os.path.abspath(inspect.getfile(func)) +', '+ func.__name__) #primary key taken as path+function name

        if primary_key not in d: #check if that primary key is in the dictionary
            d[primary_key] = end-start
        else:
            d[primary_key] = d[primary_key] + (end-start) #add the time if it occurs more than once

        
        fileread = open('exec.log', 'r') #makes the duplicate  line as empty string so it canbe updated
        listread = fileread.readlines()
        for line in range(len(listread)):
            if primary_key in listread[line]:
                listread[line] = ''
        fileread.close()


        fileopen = open('exec.log', 'w') #writes the updated value back t the exec.log
        for line in listread:
            fileopen.write(line)
        fileopen.close()
        
                
        logging.info('%s, %s ms',primary_key, (d[primary_key] * 1000)) #log our info to exec.log

        return result
    return wrap

def find_files(directory, pattern): #find files in the given directory
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
def main():

    filenamelist = [] #checks if file has .py extension
    for filename in find_files(argv[1], '*.py'):
        filenamelist.append(filename)

    for filename_in_loop in filenamelist:

        f =  open(filename_in_loop, 'rw+') #add lines necessary to run the decorator
        ss=f.readlines()

        lines_to_append = [] #append those lines as index in the list created
        for i in range(len(ss)):
            if 'def' in ss[i]:
                # print(ss[i])
                if 'def' in ss[0]:
                    ss.insert(0,'@time_profiler.timeis\n')
                if (i>0 and '@time_profiler.timeis\n' not in ss[i-1]):
                    lines_to_append.append(i)

        count = 0
        for i in range(len(lines_to_append)): #add the decorator using the above created list
            ss.insert(lines_to_append[i]+count, '@time_profiler.timeis\n')
            count+=1
        f.close()

        if 'import time_profiler\n' not in ss:
            ss.insert(0,'import sys\n')
            ss.insert(1,'sys.path.append(\''+os.getcwd()+'\')\n')
            ss.insert(2,'import time_profiler\n')

        with open(filename_in_loop, 'w') as fw: #write the changes to the specified file
            for line in ss:
                fw.write(line)
            fw.close()
            

if __name__ == "__main__":
    main()
