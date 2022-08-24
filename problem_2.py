import psutil
from datetime import datetime, timedelta
from time import sleep
import os
import pathlib
import json

#Class Imput_data sets how long will be CPU, memory and open files measure.
class Input_data:
    def time(self):
        self._parts_of_time = ["days", "hours", "minutes", "seconds"]
        self._seconds = []
        print("Insert time for measuring usage CPU, Memory and Files opening.")
        try:
            for part in self._parts_of_time:
            
                print("How many",part, ":")
                self._input = int(input())
        
                self._seconds.append(self._input)     
        except:
            print("Value error, please try again.")
            input_data.time()
        return self._seconds

"""        
Class Measure takes data about CPU, memories and files form psutil
and save it to json file.
"""
class Measure:
    def __init__(self, days, hours, minutes, seconds):
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
    
    def output(self, completeName):
        self._completeName = completeName

        self._file = open(self._completeName, "a")
        self._output = []
        self._start = datetime.now()
        self._stop = timedelta(days=self._days, hours=self._hours, 
                               minutes=self._minutes,seconds=self._seconds)
        self._time_area = self._start + self._stop
        while self._start < self._time_area:
            self._start = datetime.now()
            sleep(0.5)
            print("CPU, memory usage and open files are measureing...")
            self._cpu = (psutil.cpu_percent())
            self._memory_used = psutil.virtual_memory().used
            self._numbers_files = 0
            for p in psutil.process_iter():
                try:
                    files = p.open_files()
                    self._numbers_files = self._numbers_files + len(files)
                except:
                    pass
            self._output = {str(self._start):{"CPU": self._cpu, "Memory" : self._memory_used, 
                "Open files" : self._numbers_files}}
            jsonString = json.dumps(self._output)
                 
            self._file.write(jsonString)
            self._file.write("\n")    
            print("File {0} saved.".format(self._completeName))
        self._file.close()
        return print("Measuring proces done.")

#Class File adjusted path and file name for save data.
class File:
    def path(self):
        print("Script for measure CPU, memory usage and open files.")
        print("Actual directory is:", pathlib.Path().resolve(), "\n",
        "If you want insert new directory, write the name:")
        self._directory = str(input())
        if self._directory:
            try:
                os.mkdir(self._directory)
                self._new_directory = str(pathlib.Path().resolve()) + "/" + self._directory
                os.chdir("/"+str(self._new_directory))
                print("Directory created")
            except:
                print("Directory exist")
                os.chdir(self._directory)
        self._save_path = str(pathlib.Path().resolve())
        self._name_of_file = input("What is the name of the file: ")
        for file in os.walk(self._save_path):
            if str(self._name_of_file+".json") in str(file):    
                print("File with name {0} exists. Data will be added.".format(self._name_of_file+".json"))
                self._completeName = False
            else:
                self._completeName = os.path.join(self._save_path, self._name_of_file+".json")
                print(self._completeName)
                return self._completeName
        if self._completeName == False:
            print("Press \"y\" if you want continue.")
            if input(str()) == "y":
                self._completeName = os.path.join(self._save_path, self._name_of_file+".json")
                return self._completeName
            else:
                return False
        return self._completeName

file = File()
completeName = file.path()
if completeName == False:
    print("Measuring proces canceled.")
else:
    input_data = Input_data()
    imput_list_data = input_data.time()
    measure = Measure(imput_list_data[0], imput_list_data[1], 
                      imput_list_data[2], imput_list_data[3])
    measure.output(completeName)
