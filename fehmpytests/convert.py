import os,sys
import re
import glob

class Convertor():
    """ Converter 
    Converts old test-cases into new tet-cases.
    Modified by mlange806@gmail.com on June 6, 2014."""
    
    def __init__(self, new_path):
        """ Default Constructor 
        Sets the default path for the old test suite. """
        
        self.old_path = \
          '/n/swdev/FEHM_dev/VERIFICATION_linux/VERIFICATION_V3.2linux/'        
        self.new_path = new_path  
    
    def convertCase(self, name):
        """ Convert Case
        Takes a test-case 'name' from the old path and copies files to the new 
        test directory. """
        
        #Read the control file.
        os.chdir(self.old_path+name+'/input')
        control_file = self._readControlFile() 
        os.chdir('..')
        
        #Get input files.
        input_files = self._readFiles(control_file.getFiles('input'))
        
        #Get grid file
        grid_file = self._readFiles(control_file.getFiles('grid'))
        
        #Get compare files.
        os.chdir('output')
        types = ['*.avs', '*.his']
        compare_files = {}
        for t in types:
            #If the file type is avs, convert to csv.
            if t == '*.avs':
                old_format = self._readFiles(t)
                new_format = {}
                for key in old_format:
                    new_contents = self._convertFormat(key)
                    new_key = re.sub('.avs', '.csv', key)
                    new_format[new_key] = new_contents     
                compare_files.update(new_format)
                
            #Else, just read the files as they are.
            else:
                compare_files.update(self._readFiles(t))
            
        #Navigate to fehmpytest.
        os.chdir(new_path)
        
        #Create folder for test case, unless it already exists.
        try:
            self._createTestFolder(name)
        except:
            print 'ERROR: There is already a folder for this test case.'
            os._exit(0)
        
        #Write generic control file.
        self._writeControlFile(control_file)

        #Write the input and grid files
        self._writeFiles(input_files)
        self._writeFiles(grid_file)
        
        #Write the compare files.
        os.chdir('compare')
        self._writeFiles(compare_files)
        os.chdir('..')
        
        print 'Done.'
                                  
    def _readControlFile(self):    
        """ Read Control File
        Reads the control file for a test-case into a ControlFile object which
        can be copied and queried for specific files. """
        
        #Find the name of the control file.
        file_name = glob.glob('*.files')[0]
    
        #Read in the contents of the control file.
        opened_file = open(file_name)
        data = opened_file.read()
        opened_file.close()
        
        #Store the file list as a dictionary.
        files = {}
        with open(file_name) as opened_file:
            for line in opened_file:
                try:
                    #Add line to file_list if it can be split into kvpairs.
                    (key, value) = line.split(': ')
                    
                    #Tidy up the string.
                    value = re.sub('N', '*', value)
                    value = re.sub('UM', '', value)
                    value = re.sub('\n', '', value)
                    value = re.sub(' ', '', value)
                    
                    files[key] = value
                except:
                    #If the line can not be split into kvpairs, ignore.
                    pass
         
        #Create the control file object and return.           
        control_file = ControlFile(data, files)
        return control_file
        
    def _writeControlFile(self, control_file):
        """ Write Control File
        Writes the control file to the new test-suite in a format known to work
        currently. """
        
        #Open the file.
        opened_file = open('input/generic_fehmn.files', 'w')
        
        #Write the first lines.
        opened_file.write(control_file.getFiles('input')+'\n')
        opened_file.write(control_file.getFiles('grid')+'\n')
        opened_file.write(control_file.getFiles('input')+'\n')
        opened_file.write('out*.out\n\n')
        
        #Write the output lines.
        opened_file.write('history*.his\n')
        opened_file.write('countour*.con\n\n')
        
        #Write the last lines.
        opened_file.write('none\n')
        opened_file.write('0\n')
               
    def _readFiles(self, pattern):
        """ Read Files
        Given a glob pattern, reads files into a dictionary. """
    
        #Determine the input file names.
        file_names = glob.glob(pattern)
        
        #Store the contents of each input file as a dictionary.
        files = {}
        for f in file_names:
            opened_file = open(f)
            files[f] = opened_file.read()
            opened_file.close()
            
        return files
        
    def _createTestFolder(self, name):
        """ Create Test Folder
        Creates a folder called 'name' with subfolders for the files. """
        
        os.makedirs(name)
        os.chdir(name)
        os.makedirs('input')
        os.makedirs('compare')
        
    def _writeFiles(self, files):
        """ Write Files
        Given a dictionary of files, writes each file. """
        
        for key in files:  
            opened_file = open(key, 'w')
            opened_file.write(files[key])
            opened_file.close()
    
    def _convertFormat(self, filename):
        """ AVS to CSV Converter
        Takes in an AVS filename and converts it to CSV.
        Developed by mlange806@gmail.com May 29, 2014 """
        
        #Store the attributes and convert each line.
        data = []
        header = ''     
        with open(filename) as fp:
            #Read column numbers.
            first_line = fp.readline()
            first_line = first_line.split()
            column_num = int(first_line[0])
            
            #Read the column names.
            names = []
            i = 0
            while i < column_num:
                names.append(fp.readline())
                
                #Remove the extra dimension.
                names[i] = names[i].split(',')
                names[i] = names[i][0]
                
                i = i + 1
            
            #Create the header.        
            header = ', '.join(names)
                
            #For each row, change the spaces to commas.
            for line in fp:
                data.append(', '.join(line.split()))
    
        #Write the changes to the original file.
        new_format = header+'\n'  
        for line in data:
            new_format = new_format + '\n'+line
        
        return new_format
        
        
class ControlFile():
    """ Control File
    Stores file contents and the name of files by category. File contents and 
    the name of files in each category can get retrieved by get functions. """
    
    def __init__(self, data, files):
        #Initialize with file contents and dictionary of file information.
        self._data = data
        self._files = files
        
    def getData(self):
        #Returns the entire file contents.
        return self._data
        
    def getFiles(self, file_type):
        """ Get Files
        Returns glob pattern for category, i.e. 'input' or 'grid'. """
        
        #Work-around for different grid names in control file
        if file_type == 'grid':
            known_grids = ['grid', 'gridf']
            for grid in known_grids:
                if grid in self._files:
                    return self._files[grid]
                    
        #For now, there are not any other exceptions known.
        else:
            return self._files[file_type]               
                      
if __name__ == '__main__':
    #Check that a directory name was specified.
    if len(sys.argv) == 3:
        name = sys.argv[1]
        new_path = sys.argv[2]
    else:
        print "Usage: python old2new.py '<test-name>' '<old-test-location>'"
        os._exit(0)
     
    #Converts 'name' from old_test_suite to test case in fehmpytests.py. 
    convertor = Convertor(new_path)   
    convertor.convertCase(name)
    
