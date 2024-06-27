import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
data = r"fcc-forum-pageviews.csv"
df = pd.read_csv(data, index_col="date", parse_dates=[0]) 

# Clean data
top_threshold = np.quantile(df['value'], 0.975)
bottom_threshold = np.quantile(df['value'], 0.025)
df = df[(df['value'] <= top_threshold) & (df['value'] >= bottom_threshold)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'])

    # Set labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month']).mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar.plot(kind='bar', ax=ax)

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep","Oct", "Nov", "Dec"]
    df_box['month'] = pd.Categorical(df_box['month'], categories=months, ordered=True)

    # Draw box plots (using Seaborn)
    year_palette = sns.color_palette('tab20', len(df_box['year'].unique()))
    month_palette = sns.color_palette('tab20', len(months))
    
    fig, axs = plt.subplots(1, 2, figsize=(16,5))
    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=ax1, hue=df_box['year'],palette = year_palette, legend=False)
    axs[0].set_title("Year-wise Box Plot (Trend)")
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')


    sns.boxplot(x=df_box['month'], y=df_box['value'], ax=ax2, hue=df_box['month'], palette=month_palette, legend=False)
    axs[1].set_title("Month-wise Box Plot (Seasonality)")
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
