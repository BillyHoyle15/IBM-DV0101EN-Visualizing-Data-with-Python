# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 21:16:51 2019

@author: Suat
"""
#from __future__ import print_function #adds compabililty to python 2
import numpy as np #importing numpy library.
import pandas as pd #primary data structure library


#install xlrd

df_can = pd.read_excel(
        'https://ibm.box.com/shared/static/lw190pt9zpy5bd1ptyg2aw15awomz9pu.xlsx',
        sheet_name="Canada by Citizenship",
        skiprows = range(20),
        skipfooter = 2
        )

#df_can.head() # displays first 5 rows!!
#df_can.info() #gives brief info about data set
#df_can.columns.values #gives back column headers
#df_can.index.values #to get the list of indicies we use the .index parameter.

#to get the index and columns as lists, we can use the tolist() method.
#df_can.columns.tolist()
#df_can.index.tolist()

## size of dataframe (rows, columns)
#df_can.shape  

#clean the data set to remove a few unnecessary columns. 
#We can use pandas drop() method as follows:

# in pandas axis=0 represents rows (default) and axis=1 represents columns.
df_can.drop(['AREA','REG','DEV','Type','Coverage'], axis=1, inplace=True)
#df_can.head(2)

#Let us rename the columns so that they make sense. We can use 
#rename() method by passing in a dictionary of old and new names as follows:

df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent', 'RegName':'Region'}, inplace=True)
df_can.columns

df_can['Total'] = df_can.sum(axis=1)

#We can check to see how many null objects we have in the dataset as follows:
df_can.isnull().sum()

#let's view a quick summary of each column in our 
#dataframe using the describe() method.

df_can.describe()


#-----------------------------------------------------------------

#There are two ways to filter on a column name:
#
#Method 1: Quick and easy, but only works if the column name does NOT have spaces or special characters.
#
#    df.column_name 
#        (returns series)
#Method 2: More robust, and can filter on multiple columns.
#
#    df['column']  
#        (returns series)
#    df[['column 1', 'column 2']] 
#        (returns dataframe)

df_can.Country  # returns a series

df_can[['Country', 1980, 1981, 1982, 1983, 1984, 1985]] #returns a dataframe
# notice that 'Country' is string, and the years are integers. 
# for the sake of consistency, we will convert all column names to string later on.

#-------------------------------------------------------------------

### Select Row

###There are main 3 ways to select rows:

'''python
    df.loc[label]        
        #filters by the labels of the index/column
    df.iloc[index]       
        #filters by the positions of the index/column
    df.ix[label/index]  
        #filters by labels first (loc) but falls back to positions (iloc) 
        if label is not found 
'''

'''Before we proceed, notice that the defaul index of the dataset is a numeric 
range from 0 to 194. This makes it very difficult to do a query 
by a specific country. For example to search for data on Japan, 
we need to know the corressponding index value.

This can be fixed very easily by setting the 'Country' column 
as the index using set_index() method.'''

df_can.set_index('Country', inplace=True)
# tip: The opposite of set is reset. So to reset the index, 
#we can use df_can.reset_index()

## optional: to remove the name of the index
#df_can.index.name = None

'''
Example: Let us view the number of immigrants from Japan (row 87) for the following scenarios:

1. The full row data (all columns)
2. For year 2013
3. For years 1980 to 1985
'''

# 1. the full row data (all columns)
df_can.loc['Japan']

# alternate methods
df_can.iloc[87]
#df_can.ix[87] 
#df_can.ix['Japan']


# 2. for year 2013
df_can.loc['Japan', 2013]

# alternate methods
df_can.iloc[0, 36] # year 2013 is the last column, with a positional index of 36
#df_can.ix['Japan', 36]

# does not work
# df_can.ix[87, 2013]



# 3. for years 1980 to 1985
#df_can.ix[87, [1980, 1981, 1982, 1983, 1984, 1984]]

# alternate methods
df_can.loc['Japan', [1980, 1981, 1982, 1983, 1984, 1984]]
df_can.iloc[87, [3, 4, 5, 6, 7, 8]] 

'''
NOTE: In example 2, the following will throw an errror "index out of bounds":

# 2. for year 2013
df_can.ix[87, 2013]

When the column names are integers (such as the years), there is a bit of 
ambiguity when using .ix[]. pandas can not clearly distinguish whether 
we are asking for the column name 2013, or asking for the column with the 
2013th positional index.

To avoid this ambuigity, let's convert the column names 
into strings: '1980' to '2013'.
'''

df_can.columns = list(map(str, df_can.columns))
# [print (type(x)) for x in df_can.columns.values] #<-- uncomment to check type of column headers

# useful for plotting later on
years = list(map(str, range(1980, 2014)))

'''Filtering based on a criteria

To filter the dataframe based on a condition, we simply 
pass the condition as a boolean vector.

For example, Let's filter the dataframe to show the data on Asian countries 
(AreaName = Asia).'''

# 1. create the condition boolean series
condition = df_can['Continent']=='Asia'
#print (condition)

# 2. pass this condition into the dataFrame
df_can[condition]

# we can pass mutliple criteria in the same line. 
# let's filter for AreaNAme = Asia and RegName = Southern Asia

df_can[(df_can['Continent']=='Asia') & (df_can['Region']=='Southern Asia')]

# note: When using 'and' and 'or' operators, pandas requires we use '&' and '|' instead of 'and' and 'or'
# don't forget to enclose the two conditions in parentheses





'''----------------MATPLOTLIB-----------------------'''
import matplotlib as mpl
import matplotlib.pyplot as plt

#*optional: apply a style to Matplotlib.
print(plt.style.available)
mpl.style.use(['ggplot']) # optional: for ggplot-like style

'''LINE PLOTS'''
'''Case Study: In 2010, Haiti suffered a catastrophic magnitude 7.0 earthquake. 
The quake caused widespread devastation and loss of life and aout three million 
people were affected by this natural disaster. As part of Canada's humanitarian 
effort, the Government of Canada stepped up its effort in accepting refugees 
from Haiti. We can quickly visualize this effort using a Line plot:

Question: Plot a line graph of immigration from Haiti using df.plot().'''


#First, we will extract the data series for Haiti.
haiti = df_can.loc['Haiti', years] # Passing in years 1980 - 2013 to exclude the 'total' column
#haiti.head()
#haiti.plot() #plots

#pandas automatically populated the x-axis with the index values (years), and 
#the y-axis with the column values (population).
#
#Let us label the x and y axis using plt.title(), plt.ylabel(), 
#and plt.xlabel() as follows:

haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

plt.show() # Need this line to show the updates made to the figure

#We can clearly notice how number of immigrants from Haiti spiked up from 2010 
#as Canada stepped up its efforts to accept refugees from Haiti. Let us annotate 
#this spike in the plot by using the plt.text() method.

haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

# annotate the 2010 Earthquake. 
# syntax: plt.text(x, y, label)
plt.text(20, 6000, '2010 Earthquake') # see note below

plt.show() 

'''We can easily add more countries to line plot to make meaningful comparisons 
immigration from different countries.

Question: Let us compare the number of immigrants from India and China 
from 1980 to 2013.'''

#Step 1: Get the data set for China and India.
df_CI = df_can.loc[['India', 'China'], years]
#df_CI.head()

#Step 2: Plot graph. We will explicitly specify line plot by passing in 
#kind parameter to plot().

#Recall that pandas plots the indices on the x-axis and the columns as 
#individual lines on the y-axis. Since df_CI is a dataframe with the country 
#as the index and years as the columns, we must first transpose the dataframe 
#using transpose() method to swap the row and columns.

df_CI = df_CI.transpose()
#df_CI.head()

'''pandas will auomatically graph the two countries on the same graph. 
Note that we can alternatively pass a title parameter to the plot() 
method as an alternate approach to add the title.'''

df_CI.plot(kind='line')

plt.title('Immigrants from China and India')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show() 


'''
Line plot is a handy tool to display several dependent variables against one 
independent variable. However, it is recommended that no more than 5-10 lines 
on a single graph; any more than that and it becomes difficult to interpret.

Question: Compare the trend of top 5 countries that contributed the most to 
immigration to Canada
'''

#Step 1: Get the dataset. Recall that we created a Total column that 
#calculates the cumulative immigration by country. We will sort on this column
# to get our top 5 countries using pandas sort_values() method.

# inplace = True paramemter saves the changes to the original df_can dataframe
df_can.sort_values(by='Total', ascending=False, axis=0, inplace=True)

# get the top 5 entries
df_top5 = df_can.head(5)

# transpose the dataframe
df_top5 = df_top5[years].transpose() 

#df_top5

#Step 2: Plot the dataframe. To make the plot more readeable, we will change 
#the size using the figsize parameter.

df_top5.plot(kind='line', figsize=(14, 8)) # pass a tuple (x, y) size

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')

plt.show()


