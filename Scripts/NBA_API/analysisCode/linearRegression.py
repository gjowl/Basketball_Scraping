"""
Right now I have 10 Years worth of data, and I need to figure out what to do with it.

I'm going to look at some other 10 Year analyses that people have done, and see if there's anything that
might be interesting for me to look at using machine learning.

I think even just kind of taking all of this data and putting it into a training algorithm could be fun,
just to see what it comes out with. MaYbe best player throughout this time or something simple?

This runs on a given dataset

Followed the following video to learn how to use sklearn to do this: 
https://www.Youtube.com/watch?v=R15LjD8aCzc&ab_channel=DataProfessor
"""

from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import sys
import datetime

# load in chosen datafile from command line
alldata = pd.read_csv(sys.argv[1])
yCol = sys.argv[2]

# get current date
date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d")

# define save directory as the cwd + analysisDir + date
cwd = sys.path[0]
saveDir = cwd + '/' + date + '/'

# make the output directory if it doesn't exist
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

# rid of unnecessarY columns
data = alldata.iloc[:,5:67]

# split x and Y data 
Y = data.filter([yCol])
X = data.drop([yCol], axis=1)

# the below code will run the linear regression model on the data
# split data into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# look at data dimensions
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

# assign model function to variable
model = linear_model.LinearRegression()

# fit the model to the training data
model.fit(X_train, Y_train)

# make predictions on the test data
Y_pred = model.predict(X_test)

# output the model coefficients
print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)
print(model.score(X_test, Y_test))
print('Mean squared error (MSE): %2f' % mean_squared_error(Y_test, Y_pred))
print('Coefficient of determination (R^2): %2f'% r2_score(Y_test, Y_pred))

# Y = coefficients[0](var1) + coefficients[1](var2) + ... + intercept; coefficients are the weights for each of the variables and intercept is the y-intercept
#Y_test = pd.DataFrame(Y_test)
#print(Y_test.type)
Y_test = Y_test.to_numpy()
#Y_pred = Y_pred.flatten()
Y_test = Y_test.tolist()
Y_pred = Y_pred.tolist()

# make scatterplot

# define output file for scatterplot
scatterplotFile = saveDir + 'scatterplot.png'
plt.scatter(Y_test, Y_pred)
# save scatterplot
plt.savefig(scatterplotFile)
# trying to fix seaborn issue: https://stackoverflow.com/questions/71577514/valueerror-per-column-arrays-must-each-be-1-dimensional-when-trying-to-create-a
#sns.scatterplot(x=Y_test, y=Y_pred)
#sns.scatterplot(Y_test, Y_pred, alpha=0.5)# alpha is the transparency of the points; lowering will help see more dense points more clearly