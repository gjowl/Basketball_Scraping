import pandas as pd

# gonna have to change the naming structure for these directories when bringing in files:
# mainDir+date/dataType/Year.csv

# get date from command line
date = sys.argv[1]

# define directory to look in
directory =  date + '/'

# get the type of data to look at
dataType = sys.argv[2]
dataTypeDir = directory + dataType + '/'

# get all files in directory
files = os.listdir(directory)

# loop through files and compile data into a csv file
for f in files:
    # get file name
    filename = f.split('.')[0]
    # get file extension
    filetype = f.split('.')[1]
    # check if file is csv
    if filetype == 'csv':
        # read in file
        data = pd.read_csv(directory + f)
        # check if this is the first file
        if filename == 'data':
            # if this is the first file, just assign it to the data variable
            data = data
        else:
            # if this is not the first file, append it to the data variable
            data = data.append(data)
