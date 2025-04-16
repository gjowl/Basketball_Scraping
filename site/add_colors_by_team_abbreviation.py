from functions import change_to_team_colors
import os
import pandas as pd

# read in the data and add in the colors for the team for each player
colors = '/mnt/d/github/Basketball_Scraping/site/team_colors_hex.csv'

# read in the team colors
team_colors = pd.read_csv(colors)

data_dir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD'
# make a new directory to save the data to
output_dir = '/mnt/h/NBA_API_DATA/BOXSCORES/OLD/with_colors'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# get the data that you want to add colors to
for root, dirs, files in os.walk(data_dir):
    # read in the data
    for file in files:
        # look if the name of the file is what you want
        datafile = os.path.join(root, file)
        data = pd.read_csv(datafile)
        colors_1, colors_2 = [], []
        # add in the team color for each player
        filename = file.split('.')[0]
        for i in range(len(data)):
            # get the team abbreviation and match it to the hexcolors file
            team = data['TEAM_ABBREVIATION'][i]
            # get the color from the team_colors file
            color1 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 1'].values[0]
            color2 = team_colors[team_colors['TEAM_ABBREVIATION'] == team]['Color 2'].values[0]
            colors_1.append(color1)
            colors_2.append(color2)
        data['Color 1'] = colors_1
        data['Color 2'] = colors_2
        # save the data to a new file
        data.to_csv(os.path.join(output_dir, f'{filename}.csv'), index=False)