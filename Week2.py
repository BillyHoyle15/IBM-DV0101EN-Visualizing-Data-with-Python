# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 14:36:44 2019

@author: Suat
"""

'''IMPORTANT NOTE: UNCOMMENT THE PART THAT YOU'RE GOING TO USE AND COMMENT
AGAIN BEFORE NEW PLOT'''

from __future__ import print_function # this line adds compatibility to python 2
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library

#Let us download and import our primary Canadian Immigration dataset 
#using pandas read_excel() method.

#before that be sure that you have xlrd module for excel.

'''Download the data set and inser into pandas dataframe df_can
sheetname changed into --> sheet_name
skip_footer changed into --> skipfooter'''
df_can = pd.read_excel('https://ibm.box.com/shared/static/lw190pt9zpy5bd1ptyg2aw15awomz9pu.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2
                      )


##Below is looking for first five rows of the dataset
#df_can.head()

## print the dimensions of the dataframe
print(df_can.shape)

#Clean up data. We will make some modifications to the original dataset to 
#make it easier to create our visualizations.

#delette some unneccesary columns
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)

#renaming columns for more sense
df_can.rename(columns={'OdName':'Country', 'AreaName':'Continent','RegName':'Region'}, inplace=True)

# let's examine the types of the column labels
all(isinstance(column, str) for column in df_can.columns)

#Notice how the above line of code returned False when we tested if all the 
#column labels are of type string. So let's change them all to string type.

#change column names into string
df_can.columns = list(map(str, df_can.columns))

## 4. Set the country name as index - useful for quickly looking up 
##countries using .loc method.
df_can.set_index('Country', inplace=True)

## Add total column.
df_can['Total'] = df_can.sum(axis=1) #remember axis=0 -->rows, axis=0-->columns

# finally, let's create a list of years from 1980 - 2014
# this will come in handy when we start plotting the data
years = list(map(str, range(1980, 2014)))


'''IMPORTANT: DO YOUR IMPORTS AT THE BEGINNING OF THE FILE'''
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.style.use('ggplot') # optional: for ggplot-like style


'''-----------------------------AREA PLOTS--------------------------------'''
##We can visualize line plot as a cumulative plot, also knows as a 
##Stacked Line Plot or Area plot.

#sort Total values from bigger to smaller
df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)

# get the top 5 entries into a new dataframe
df_top5 = df_can.head(5)

# transpose the dataframe because otherwise plot won't make sense
df_top5 = df_top5[years].transpose() 


#Area plots are stacked by default. And to produce a stacked area plot, 
#each column must be either all positive or all negative values (any NaN values, 
#will defaulted to 0). To produce an unstacked plot, pass stacked=False.

#df_top5.plot(kind='area', 
#             stacked=False, #try true
#             figsize=(20, 9), # pass a tuple (x, y) size
#            ) 
#
#plt.title('Immigration Trend of Top 5 Countries')
#plt.ylabel('Number of Immigrants')
#plt.xlabel('Years')
#
#plt.show()


#The unstacked plot has a default transparency (aplha value) at 0.5. 
#We can modify this value by passing in the alpha parameter.

#df_top5.plot(kind='area', 
#             alpha=0.25, # 0-1, default value a= 0.5
#             stacked=False,
#             figsize=(20, 9),
#            )
#
#plt.title('Immigration Trend of Top 5 Countries')
#plt.ylabel('Number of Immigrants')
#plt.xlabel('Years')
#
#plt.show()


'''------------------------------HISTOGRAMS-----------------------------'''
#A histogram is a way of representing the frequency distribution of numeric 
#data set. The way it works is it partitions the x-axis into bins, assigns each 
#data point in our dataset to a bin, and then counts the number of data points 
#that have been assigned to each bin. So the y-axis is the frequency or the 
#number of data points in each bin. Note that we can change the bin size and 
#usually one needs to tweak it so that the distribution is displayed nicely.
#
#Question: What is the frequency distribution of the number (population) of 
#new immigrants from the various countries to Canada in 2013?
#
#Before we proceed with creating the histogram plot, let us first examine the 
#data split into intervals. To do this, we will us Numpy's histrogram method to 
#get the bin ranges and frequency counts as follows:

# np.histogram returns 2 values
count, bin_edges = np.histogram(df_can['2013']) #automatically 10 partitions

print('count is: ',count) # frequency count
print('bin ranges: ',bin_edges) # bin ranges, default = 10 bins

#plotting
#df_can['2013'].plot(kind='hist', figsize=(8, 5))
#
#plt.title('Histogram of Immigration from 195 Countries in 2013') # add a title to the histogram
#plt.ylabel('Number of Countries') # add y-label
#plt.xlabel('Number of Immigrants') # add x-label
#
#plt.show() #don't foreget to comment out plots for Area Plots

#In the above plot, the x-axis represents the population range of immigrants in 
#intervals of 3412.9. The y-axis represents the number of countries that 
#contributed to the aforementioned population.
#
#Notice that the x-axis labels do not match with the bin size. This can be 
#fixed by passing in a xticks keyword that contains the list of the bin sizes, 
#as follows:

# 'bin_edges' is a list of bin intervals
#count, bin_edges = np.histogram(df_can['2013'])
#
#df_can['2013'].plot(kind='hist', figsize=(8, 5), xticks=bin_edges)
#
#plt.title('Histogram of Immigration from 195 countries in 2013') # add a title to the histogram
#plt.ylabel('Number of Countries') # add y-label
#plt.xlabel('Number of Immigrants') # add x-label
#
#plt.show()

#We can also plot multiple histograms on the same plot. For example, 
#let's try to answer the following questions using a histogram.
#
#Question: What is the immigration distribution for Denmark, Norway, and 
#Sweden for years 1980 - 2013?

# let's quickly view the data set 
df_can.loc[['Denmark', 'Norway', 'Sweden'], years]

# generate histogram
#df_can.loc[['Denmark', 'Norway', 'Sweden'], years].plot.hist()

#That(above) does not look right!
#
#Don't worry, you'll often come across situations like this when creating plots.
#The solution often lies in how the underlying dataset is structured.
#
#Instead of plotting the population frequency distribution of the population 
#for the 3 countries, pandas instead plotted the population frequency 
#distribution for the years.
#
#This can be easily fixed by first transposing the dataset, and then plotting 
#as shown below.

# transpose dataframe
#df_t = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()
#
## generate histogram
#df_t.plot(kind='hist', figsize=(10, 6))
#
#plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
#plt.ylabel('Number of Years')
#plt.xlabel('Number of Immigrants')
#
#plt.show()

#Let us make a few modifications to improve the impact and aesthetics of the 
#previous plot:
#
#***increase the bin size to 15 by passing in bins parameter
#***set transparency to 60% by passing in alpha paramemter
#***label the x-axis by passing in x-label paramater
#***change the colors of the plots by passing in color parameter

# Let's get the x-tick values
#count, bin_edges = np.histogram(df_t, 15)

# Un-stacked Histogram
#df_t.plot(kind ='hist', 
#          figsize=(10, 6),
#          bins=15,
#          alpha=0.6,
#          xticks=bin_edges,
#          color=['coral', 'darkslateblue', 'mediumseagreen']
#         )
#
#plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
#plt.ylabel('Number of Years')
#plt.xlabel('Number of Immigrants')
#
#plt.show()

##Tip: For a full listing of colors available in Matplotlib, run the following 
##code in your python shell:

##import matplotlib
##for name, hex in matplotlib.colors.cnames.items():
##    print(name, hex)


#If we do no want the plots to overlap each other, we can stack them using the 
#stacked paramemter. Let us also adjust the min and max x-axis labels to remove 
#the extra gap on the edges of the plot. We can pass a tuple (min,max) using the 
#xlim paramater, as show below.

#count, bin_edges = np.histogram(df_t, 15)
#xmin = bin_edges[0] - 10   #  first bin value is 31.0, adding buffer of 10 for aesthetic purposes 
#xmax = bin_edges[-1] + 10  #  last bin value is 308.0, adding buffer of 10 for aesthetic purposes

#Stacked Histogram
#df_t.plot(kind='hist',
#          figsize=(10, 6), 
#          bins=15,
#          xticks=bin_edges,
#          color=['coral','darkslateblue','mediumseagreen'],
#          stacked=True,
#          xlim=(xmin,xmax)
#         )
#
#plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
#plt.ylabel('Number of Years')
#plt.xlabel('Number of Immigrants') 
#
##plt.show() #uncomment when plotting



'''------------------------------BAR CHARTS-------------------------------'''
#A bar plot is a way of representing data where the length of the bars 
#represents the magnitude/size of the feature/variable. Bar graphs usually 
#represent numerical and categorical variables grouped in intervals.
#
#To create a bar plot, we can pass one of two arguments via kind 
#parameter in plot():
#
#kind=bar creates a vertical bar plot
#kind=barh creates a horizontal bar plot
#Vertical bar plot
#
#In vertical bar graphs, the x-axis is used for labelling, and the length of 
#bars on the y-axis corresponds to the magnitude of the variable being measured. 
#Vertical bar graphs are particuarly useful in analyzing time series data. 
#One disadvantage is that they lack space for text labelling at the foot of 
#each bar.
#
#Let us start off by analyzing the effect of Iceland's Financial Crisis:
#
#The 2008 - 2011 Icelandic Financial Crisis was a major economic and political 
#event in Iceland. Relative to the size of its economy, Iceland's 
#systemic banking collapse was the largest experienced by any country in 
#economic history. The crisis led to a severe economic depression in 2008 - 2011 
#and significant political unrest.
#
#Question: Let us compare the number of Icelandic 
#immigrants (country = 'Iceland') to Canada from year 1980 to 2013.

# step 1: get the data
#df_iceland = df_can.loc['Iceland', years]
#
## step 2: plot data
#df_iceland.plot(kind='bar', figsize=(10, 6))
#
#plt.xlabel('Year') # add to x-label to the plot
#plt.ylabel('Number of immigrants') # add y-label to the plot
#plt.title('Icelandic immigrants to Canada from 1980 to 2013') # add title to the plot
#
#plt.show() #again, comment out other plt.show() commands

#The bar plot above shows the total number of immigrants broken down by each 
#year. We can clearly see the impact of the financial crisis; the number of 
#immigrants to Canada started increasing rapidly after 2008.


#Let us annotate this on the plot using the annotate method of the scripting 
#layer or the pyplot interface. We will pass in the following parameters:
#
#s: str, the text of annotation.
#xy: Tuple specifying the (x,y) point to annotate (in this case, end point of 
#                         arrow).
#xytext: Tuple specifying the (x,y) point to place the text (in this case, 
#                             start point of arrow).
#xycoords: The coordinate system that xy is given in - 'data' uses the 
#          coordinate system of the object being annotated (default).
#arrowprops: Takes a dictionary of properties to draw the arrow:
#arrowstyle: Specifies the arrow style, '->' is standard arrow.
#connectionstyle: Specifies the connection type. arc3 is a straight line.
#color: Specifes color of arror.
#lw: Specifies the line width.
#
#I encourage you to read the Matplotlib documentation for more details on 
#annotations: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.annotate.

#df_iceland.plot(kind='bar', figsize=(10, 6), rot=90) # rotate the bars by 90 degrees
#
#plt.xlabel('Year')
#plt.ylabel('Number of Immigrants')
#plt.title('Icelandic Immigrants to Canada from 1980 to 2013')

# Annotate arrow
#plt.annotate('',                      # s: str. Will leave it blank for no text
#             xy=(32, 70),             # Place head of the arrow at point (year 2012 , pop 70 )
#             xytext=(28, 20),         # Place base of the arrow at point (year 2008 , pop 20 )
#             xycoords='data',         # Will use the coordinate system of the object being annotated 
#             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)
#            )
#
#plt.show()


#Let us also annotate a text to go over the arrow. We will pass in the following 
#additional parameters:
#
#rotation: rotation angle of text in degrees (counter clockwise)
#va: vertical alignment of text [‘center’ | ‘top’ | ‘bottom’ | ‘baseline’]
#ha: horizontal alignment of text [‘center’ | ‘right’ | ‘left’]

#df_iceland.plot(kind='bar', figsize=(10, 6), rot=90) 
#
#plt.xlabel('Year')
#plt.ylabel('Number of Immigrants')
#plt.title('Icelandic Immigrants to Canada from 1980 to 2013')

# Annotate arrow
#plt.annotate('',                      # s: str. Will leave it blank for no text
#             xy=(32, 70),             # place head of the arrow at point (year 2012 , pop 70 )
#             xytext=(28, 20),         # place base of the arrow at point (year 2008 , pop 20 )
#             xycoords='data',         # will use the coordinate system of the object being annotated 
#             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)
#            )
#
## Annotate Text
#plt.annotate('2008 - 2011 Financial Crisis', # text to display
#             xy=(28,30),                   # start the text at at point (year 2008 , pop 30)
#             rotation=72.5,                # Based on trial and error to match the arrow
#             va='bottom',                  # Want the text to be vertically 'bottom' aligned
#             ha='left',                    # Want the text to be horizontally 'left' algned.
#            )
#
#plt.show()


'''---Horizontal Bar Plot---'''

#Sometimes it is more practical to represent the data horizontally, especially 
#if you need more room for labelling the bars. In horizontal bar graphs, 
#the y-axis is used for labelling, and the length of bars on the x-axis 
#corresponds to the magnitude of the variable being measured. 
#As you will see, there is more room on the y-axis to label categetorical 
#variables.
#
#Question: Using the df_can dataset, create a horizontal bar plot showing the 
#total number of immigrants to Canada from the top 15 countries, for the period 
#1980 - 2013. Label each country with the total immigrant count.

#Step 1: Get the data.
# sort dataframe on 'Total' column (descending)
df_can.sort_values(by='Total', ascending=True, inplace=True)

# get top 15 countries
df_top15 = df_can['Total'].tail(15)

#Step 2: Plot data. We will use a for loop to cycle through the countries 
#and annotate the immigrant population.

# generate plot
df_top15.plot(kind='barh', figsize=(12, 12), color='steelblue')
plt.xlabel('Number of Immigrants')
plt.title('Top 15 Conuntries Contributing to the Immigration to Canada between 1980 - 2013')

# annotate value labels to each country
for index, value in enumerate(df_top15): 
    label = format(int(value), ',') # format int with commas
    
    # place text at the end of bar (subtracting 47000 from x, and 0.1 from y to make it fit within the bar)
    plt.annotate(label, xy=(value - 47000, index - 0.10), color='white')
    
plt.show() #agaib, comment out above plots

