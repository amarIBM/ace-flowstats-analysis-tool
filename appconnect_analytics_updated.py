# Copyright 2022 IBM Corporation 
# Author: Amar Shah
 
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the MIT License
#  which accompanies this distribution, and is available at
#  http://opensource.org/licenses/MIT
 
#  Contributors:
#      Amar Shah, Hina Sharma,  Anshu Garg

# Import the required libraries
import base64
import getopt
import io
import os
from io import StringIO, BytesIO
import matplotlib as mpl, matplotlib.pyplot as plt
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import dates
import seaborn as sns
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.colors import LinearSegmentedColormap
from plotly.subplots import make_subplots
import plotly.graph_objs as go

import consolidate
from pylab import *
from tabulate import tabulate
fpath=""
dirname = os.path.dirname(__file__)
dirname1=os.path.join(dirname,"static")
# Global
plt.style.use("ggplot")
'''
indir = 'C:/Users/ANSHU/ML/AppConnect/Logs/*'
outdir = 'C:/Users/ANSHU/ML/AppConnect/Output'
topnum = 3
showgroup = 'yes'
'''
indir = ''
outdir = ''
topnum = ''
showgroup = 'yes'
msgFlowCount=0
created_df=pd.DataFrame()
df_topMessageFlows=pd.DataFrame()
df_topmsg_records=pd.DataFrame()

cmapGR = LinearSegmentedColormap(
    'GreenRed',
        {
            'red': ((0.0, 0.0, 0.0),
                    (0.5, 1.0, 1.0),
                    (1.0, 1.0, 1.0)),
            'green': ((0.0, 1.0, 1.0),
                      (0.5, 1.0, 1.0),
                      (1.0, 0.0, 0.0)),
            'blue': ((0.0, 0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (1.0, 0.0, 0.0))
        },
    )


def init(odir):
    df = pd.read_csv(os.path.join(odir, 'joined.csv'), index_col=['StartTimeStampLambda'], parse_dates=True)
    df.index = pd.to_datetime(df.index, errors="coerce")
    df = df[['Message Flow Name', 'Average Elapsed Time_flow', 'Average CPU Time_flow', 'Node Name', 'Node Type',
             'Average Elapsed Time', 'Average CPU Time', 'Total Number of Input Messages', 'EndTimeStampLambda']]
    return df

def msgflwcnt(rdf):
    msgFlowCount = rdf['Message Flow Name'].nunique(dropna=True)
    print("Total number of unique message flows: ", msgFlowCount)
    if msgFlowCount >= 3:
        msgFlowCount=3
    return msgFlowCount

def flask_elapsed_graph(rdf,msgFlowCount):
    df_avg_MessageFlow_Elapsed = rdf.groupby(['Message Flow Name']).agg({'Average Elapsed Time_flow': ['mean']})
    df_topMessageFlows = df_avg_MessageFlow_Elapsed.head(
        msgFlowCount).sort_values([('Average Elapsed Time_flow', 'mean')],
                                  ascending=False)
    df_topMessageFlows[('Average Elapsed Time_flow', 'mean')] = \
    df_topMessageFlows[('Average Elapsed Time_flow', 'mean')].round(decimals=1)

    fig, ax = plt.subplots(2)
    ax[0] = df_topMessageFlows.plot(kind='bar', rot=90)
    ax[0].legend(["Average Elapsed Time_flow"])
    ax[0].set_ylabel("Average Elapsed Time(ms)")

    for p in ax[0].patches:
        ax[0].annotate(str(p.get_height()),
                    (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.savefig(os.path.join(dirname1,"messageflow_elapse.png"),
                bbox_inches="tight")

    df_avg_MessageFlow_CPU = rdf.groupby(['Message Flow Name']).agg(
        {'Average CPU Time_flow': ['mean']})
    df_topMessageFlows_CPU = df_avg_MessageFlow_CPU.head(
        msgFlowCount).sort_values([(
        'Average CPU Time_flow', 'mean')], ascending=False)
    df_topMessageFlows_CPU[('Average CPU Time_flow', 'mean')] = \
    df_topMessageFlows_CPU[('Average CPU Time_flow', 'mean')].round(decimals=1)
    print("df_topMessageFlows_CPU values are ", df_topMessageFlows_CPU)
    ax[1] = df_topMessageFlows_CPU.plot(kind='bar', rot=90)
    ax[1].legend(["Average CPU Time_flow"])
    ax[1].set_ylabel("Average CPU Time(ms)")
    for p in ax[1].patches:
        ax[1].annotate(str(p.get_height()),
                    (p.get_x() * 1.005, p.get_height() * 1.005))

    plt.savefig(os.path.join(dirname1,"messageflow_cpu1.png"),
                bbox_inches="tight")

    return df_topMessageFlows, df_topMessageFlows_CPU


def allrecords_topmsgflow_elapsed(rdf,msgFlowCount):
    fig, ax =plt.subplots()
    df_avg_MessageFlow_Elapsed = rdf.groupby(['Message Flow Name']).agg(
        {'Average Elapsed Time_flow': ['mean']})
    df_topMessageFlows = df_avg_MessageFlow_Elapsed.head(
        msgFlowCount).sort_values([('Average Elapsed Time_flow', 'mean')],
                                  ascending=False)
    df_topmsg_records = df_topMessageFlows.head(
        msgFlowCount).index.tolist()

    # All records for the top three message flows
    df_msg = rdf[rdf['Message Flow Name'].isin(df_topmsg_records)]
    for i in range(0, msgFlowCount):
        # Mean of average elapsed time for the message flows

        df_msgflow_allrecords = df_msg[df_msg['Message Flow Name'] ==
                                       df_topmsg_records[i]]
        x = df_msgflow_allrecords['Average Elapsed Time_flow'].mean()
        print ('df_msgflow_allrecords.head(5)',df_msgflow_allrecords.head(5) )
        print("Mean of Message Flow %s is %d" %(df_topmsg_records[i], x))

        plt.title("Average Elapsed Time for " + df_topmsg_records[i])
        ax = df_msgflow_allrecords.plot(rot=45, figsize=(15, 10),
                                               title=df_topmsg_records[
                                                   i])
        ax.xaxis.set_major_locator(dates.MinuteLocator(interval=300))
        ax.set_ylabel("Average Elapsed Time_flow")
        #return df_msgflow_allrecords
        return df_topmsg_records

def allrecords_topmsgflow_cpu(rdf,msgFlowCount):
    for i in range (1, msgFlowCount+1):
        df_topmsg_CPU = df_topmsg_records[
            df_topmsg_records['Message Flow Name'] ==
            df_topmsg_records[i]]
        df_topmsg_CPU = df_topmsg_CPU[
            'Average CPU Time_flow'].sort_values(ascending=False)
        x = df_topmsg_CPU.mean()
        print("Mean of Message Flow %s is %d" % (df_topmsg_CPU[i], x))

        # Plot the average elapsed and cpu times
        plt.title("Average CPU Time for " + df_topmsg_records[i])
        ax = df_topmsg_CPU.plot(rot=45, figsize=(15, 10),
                                                    title=
                                                    df_topmsg_records[i])
        ax.xaxis.set_major_locator(dates.MinuteLocator(interval=600))
        ax.set_ylabel("Average CPU Time_flow")

def msg_node_concat():
    rdf = created_df.copy()
    rdf['concat'] = rdf["Node Name"].astype(str) + '-' + rdf["Node Type"]
    dfg = rdf.groupby(['Message Flow Name', 'concat']).agg(
        {'Average Elapsed Time': ['mean'],
         'Average CPU Time': 'mean'})
    g = dfg.groupby(level=0, group_keys=False).apply(
        lambda y: y.sort_values(('Average Elapsed Time', 'mean'),
                                ascending=False).head(5))
    print(g)
    df_avg_nodename_type_avg_cpu = rdf.groupby(['concat']).agg(
        {'Average CPU Time': ['mean', 'min', 'max', 'size']})
    df_avg_nodename_type_avg_cpu1 = df_avg_nodename_type_avg_cpu.sort_values(
        [('Average CPU Time', 'mean')], ascending=False)


def msg_input_vs_elapsedtime(rdf,df_topmsg_records,msgFlowCount):
   img = BytesIO()
   df_topmsg_input=pd.DataFrame()
   fig  = make_subplots(rows=2, cols=2, specs=[[{"secondary_y": True},
                                                   {"secondary_y": True}],
                              [{"secondary_y": True}, {"secondary_y":
                                                           True}]],
                        subplot_titles=(df_topmsg_records[0],
                                        df_topmsg_records[1],df_topmsg_records[
                                            2]))
   for i in range(0, msgFlowCount):
        print("Value of df_topmsg_records", df_topmsg_records)
        df_topmsg_input = rdf[rdf['Message Flow Name'] == df_topmsg_records[i]]
        subplots_adjust(left=0.25)
        subplots_adjust(bottom=0.25)

        plt.title("Input Message vs Elapsed Time")
        print("Value of df_topmsg_input",df_topmsg_input)

        if i==0:
            fig.add_trace(
               go.Scatter(x=df_topmsg_input.index,
                          y=df_topmsg_input['Total Number of Input Messages'],
                          name="Total Number of Input Messages",
                          mode='lines',line=dict(color='royalblue',width=2),
                          showlegend=True),
               row=1, col=1, secondary_y=False)
            fig.add_trace(
                go.Scatter(x=df_topmsg_input.index,
                           y=df_topmsg_input['Average Elapsed Time_flow'],
                           name="Average Elapsed Time",mode='lines',
                           line=dict(color='firebrick',width=2),
                           showlegend=True),
                row=1, col=1, secondary_y=True)

        if i==1:
            fig.add_trace(
                go.Scatter(x=df_topmsg_input.index,
                           y=df_topmsg_input['Total Number of Input Messages'],
                           mode='lines',line=dict(color='royalblue',width=2),showlegend=False),
                row=1, col=2, secondary_y=False)
            fig.add_trace(
                go.Scatter(x=df_topmsg_input.index,
                           y=df_topmsg_input['Average Elapsed Time_flow'],
                           mode='lines',line=dict(color='firebrick',width=2),showlegend=False),
                row=1, col=2, secondary_y=True)
        if i==2:
           # Bottom left
            fig.add_trace(
                go.Scatter(x=df_topmsg_input.index,
                           y=df_topmsg_input['Total Number of Input Messages'],
                           mode='lines',line=dict(color='royalblue',width=2),showlegend=False),
                row=2, col=1, secondary_y=False)
            fig.add_trace(
                go.Scatter(x=df_topmsg_input.index,
                           y=df_topmsg_input['Average Elapsed Time_flow'],
                           name="Average Elapsed Time_flow",mode='lines',
                           line=dict(color='firebrick',width=2),showlegend=False),
                row=2, col=1, secondary_y=True)

   #return df_topmsg_input
   fig.update_xaxes(title_text="Date")

   fig.update_yaxes(title_text="No. of Input Messages", secondary_y=False)
   fig.update_yaxes(title_text="Average Elapsed Time", secondary_y=True)


   fig.update_layout(
       xaxis_title='Date',
       height=500,
       margin= dict(
       l=10,
       r=50,
       t=50,
       b=10

   )
   )

   return fig


def msg_heatmap_hourly(rdf,df_topmsg_records,msgFlowCount):
    # Add heatmap code here
    plt.figure(0)

    fig, axs = plt.subplots(5)

    for i in range(0, msgFlowCount):

        daily_average=pd.DataFrame()
        daily_average = rdf[rdf['Message Flow Name'] == df_topmsg_records[i]].resample('H').mean()
        daily_average.to_csv(os.path.join(outdir, 'DateMean_message1.csv'))
        daily_average = pd.read_csv(os.path.join(outdir,
                                                 'DateMean_message1.csv'), parse_dates=True)
        daily_average['StartTimeStampLambda'] = pd.to_datetime(daily_average['StartTimeStampLambda'])
        daily_average['Dates'] = daily_average['StartTimeStampLambda'].dt.date
        daily_average['Time1'] = daily_average['StartTimeStampLambda'].dt.time
        daily_average['Average Elapsed Time'] = daily_average['Average Elapsed Time'] * .001
        daily_average = daily_average[daily_average['Average Elapsed Time'].notna()]
        daily_average = daily_average.reset_index(drop=True)
        df1 = daily_average[['Time1', 'Dates', 'Average Elapsed Time']]
        print(df_topmsg_records[i], df1.head(5))
        heatmap_pt1 = pd.pivot_table(df1, values='Average Elapsed Time', index=['Time1'], columns='Dates')
        print("heatmap",heatmap_pt1)
        axs[i] = sns.heatmap(heatmap_pt1, annot=True, fmt="g",cmap=cmapGR,
                             cbar_kws={
                'label': 'Average Elapsed Time range'})
        axs[i].legend(["Average Elapsed Time_flow"])
        axs[i].set_ylabel("Elapsed Time")
        axs[i].set_title(df_topmsg_records[i])
        plt.close(4)
        plt.close(5)
        # plt.tight_layout()
        plt.savefig(os.path.join(dirname1, "final%d.png" % i))
        plt.clf()
        if i==0:
            heatmap_pt1 = pd.pivot_table(df1, values='Average Elapsed Time',
                                         index=['Time1'], columns='Dates')
            axs[i] = sns.heatmap(heatmap_pt1,annot=True, fmt="g",cmap=cmapGR,
                                 cbar_kws={
                'label': 'Average Elapsed Time range'})
            axs[i].legend(["Average Elapsed Time_flow"])
            axs[i].set_ylabel("Elapsed Time")
            axs[i].set_title(df_topmsg_records[i])
            print(df_topmsg_records[i], df1.head(5))
            plt.savefig(os.path.join(dirname1, "final6.png"))
            plt.clf()

def main(argv):
    indir = 'C:/Users/ANSHU/ML/AppConnect/Logs/*'
    outdir = 'C:/Users/ANSHU/ML/AppConnect/Output'
    topnum = 10
    showgroup = 'yes'

    try:
        opts, args = getopt.getopt(argv, "hi:o:t:g:", ["idir=", "odir=", "top=", "showgrouped="])
    except getopt.GetoptError:
        print('consolidate.py -i <inputdir> -o <outputdir> -t 20 -g <yes/no>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('consolidate.py -i <inputdir> -o <outputdir>  -t 20 -g <yes/no> ')
            sys.exit()
        elif opt in ("-i", "--idir"):
            indir = arg
        elif opt in ("-o", "--odir"):
            outdir = arg
        elif opt in ("-t", "--top"):
            topnum = arg
        elif opt in ("-g", "--showgrouped"):
            showgroup = arg
    # Consolidate logs
    consolidate.join_logs(indir, outdir, topnum, showgroup)

    # Initialize flow-node joined dataframe
    created_df = init(outdir)
    return created_df



# if __name__ == '__main__':
#     main(sys.argv[1:])
