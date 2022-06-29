# Copyright 2022 IBM Corporation 
# Author: Amar Shah
 
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the MIT License
#  which accompanies this distribution, and is available at
#  http://opensource.org/licenses/MIT
 
#  Contributors:
#      Amar Shah, Hina Sharma,  Anshu Garg

import types
import pandas as pd
import os
import sys
import glob
from pathlib import Path
import shutil

def join_logs(idir, odir, top, showgrouped):
    dir = 'C:/Users/ANSHU/ML/AppConnect/Logs/*'
    outdir = 'C:/Users/ANSHU/ML/AppConnect/Output/'
    numlist = 10
    showgroupeddata = 'yes'

    if idir:
        dir = idir
    if odir:
        outdir = odir
    if top:
        numlist = top
    if showgrouped:
        showgroupeddata = showgrouped
    print("************************")
    print(dir, outdir, numlist, showgroupeddata)
    dirpath = Path(outdir)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    if os.path.exists(os.path.join(outdir, 'flow.csv')):
        os.remove(os.path.join(outdir, 'flow.csv'))
    if os.path.exists(os.path.join(outdir, 'node.csv')):
        os.remove(os.path.join(outdir, 'node.csv'))
    if os.path.exists(os.path.join(outdir, 'joined.csv')):
        os.remove(os.path.join(outdir, 'joined.csv'))

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    flowfilename = '*flowStats*csv*'
    nodefilename = '*nodeStats*csv*'


    flowcount = 0
    nodecount = 0
    print("dir",dir)
    print("flowfilename",flowfilename)
    # read flow files
    temp_flow = []
    for name in glob.glob(dir + '/' + flowfilename):
        print("name",name)
        df = pd.read_csv(name, index_col=None, header=0)
        flowcount = flowcount + df.shape[0]
        print("flowcount", flowcount)
        temp_flow.append(df)

    # merge flow files
    df_flow = pd.concat(temp_flow, axis=0, ignore_index=True)

    # Drop few columns
    df_flow.drop(['Record Type', 'Record Code', 'Broker UUID', 'EG UUID', 'Message Flow UUID', 'Application Name',
                  'Application UUID', 'Library Name', 'Library UUID', 'Record Start Date', 'Record Start Time',
                  'Record End Date', 'Record End Time', 'Accounting Origin'], axis=1, inplace=True)

    df_flow['EndTimeStampLambda'] = df_flow.apply(lambda x: str(x['Record GMT End Timestamp']).split(".")[0], axis=1)
    # Drop milliseconds  and create new attribute
    df_flow['StartTimeStampLambda'] = df_flow.apply(lambda x: str(x['Record GMT Start Timestamp']).split(".")[0],
                                                    axis=1)

    # Save flow file
    # df_flow.to_csv (r'/ML/Output/flow.csv', index = False, header=True)
    df_flow.to_csv(r'%s/flow.csv' % outdir, index=False, header=True)
    print('************************Total flow rows count = %s ************************' % flowcount)
    # print('df flow shape = %s' % df_flow.shape[0])

    # read node files
    temp_node = []
    for name in glob.glob(dir + '/' + nodefilename):
        df = pd.read_csv(name, index_col=None, header=0)
        nodecount = nodecount + df.shape[0]
        temp_node.append(df)

    # merge node files
    df_node = pd.concat(temp_node, axis=0, ignore_index=True)

    # Drop few columns
    df_node.drop(
        ['Record Type', 'Record Code', 'Application Name', 'Library Name', 'Record Start Date', 'Record Start Time',
         'Record End Date', 'Record End Time'], axis=1, inplace=True)

    # Drop milliseconds and create new attributes
    df_node['StartTimeStampLambda'] = df_node.apply(lambda x: str(x['Record GMT Start Timestamp']).split(".")[0],
                                                    axis=1)
    df_node['EndTimeStampLambda'] = df_node.apply(lambda x: str(x['Record GMT End Timestamp']).split(".")[0], axis=1)

    # Save node file
    # df_node.to_csv (r'/ML/Output/node.csv', index = False, header=True)
    df_node.to_csv(r'%s/node.csv' % outdir, index=False, header=True)
    print('***************Total node rows count = %s ************************' % nodecount)

    # Join flow and node data
    df_join = df_node.join(df_flow.set_index(['Message Flow Name', 'Broker Name', 'EG Name', 'StartTimeStampLambda']),
                           on=(['Message Flow Name', 'Broker Name', 'EG Name', 'StartTimeStampLambda']),
                           rsuffix='_flow')

    # Save joined data
    df_join.to_csv(r'%s/joined.csv' % outdir, index=False, header=True)
    # print(df_join.min())
    # print(df_join[df_join['Total Elapsed Time'] == df_join['Total Elapsed Time'].max()])

    # Total_Elapsed Time from merged data for node
    largest = df_join.nlargest(int(numlist), ['Total Elapsed Time'])
    print("**********************Top %s node elapsed time from merged dataset*************************" % numlist)
    print(largest['Total Elapsed Time'])
    print(
        "**********************Top %s rows with most node elapsed time from merged dataset*************************" % numlist)
    print(largest)
    largest.to_csv(r'%s/topnodeelapsedtimejoined.csv' % outdir, index=False, header=True)

    # Total Elapsed Time for flow from merged data
    flargest = df_join.nlargest(int(numlist), ['Maximum Elapsed Time_flow'])
    print("**********************Top %s flow elapsed time from merged dataset*************************" % numlist)
    print(flargest['Maximum Elapsed Time_flow'])
    print(
        "**********************Top %s rows with most flow elapsed time from merged dataset*************************" % numlist)
    print(flargest)
    flargest.to_csv(r'%s/topflowelapsedtimejoined.csv' % outdir, index=False, header=True)

    # Total Elapsed Time for flow from flow data only
    flargest = df_flow.nlargest(int(numlist), ['Total Elapsed Time'])
    print("**********************Top %s highest elapsed time from flow dataset*************************" % numlist)
    print(flargest['Total Elapsed Time'])
    print(
        "**********************Top %s rows with flow elapsed time from flow dataset*************************" % numlist)
    print(flargest)
    flargest.to_csv(r'%s/topflowelapsedtimeflow.csv' % outdir, index=False, header=True)

    # Total Elapsed Time for node from node data only
    largest = df_node.nlargest(int(numlist), ['Total Elapsed Time'])
    print("**********************Top %s node  elapsed time from node dataset*************************" % numlist)
    print(largest['Total Elapsed Time'])
    print(
        "**********************Top %s rows with highest elapsed time from node dataset*************************" % numlist)
    print(largest)
    largest.to_csv(r'%s/topnodeelapsedtimenode.csv' % outdir, index=False, header=True)

    # Highest CPU from merged data for node
    largest = df_join.nlargest(int(numlist), ['Average CPU Time'])
    print("**********************Top %s node average cpu time from merged dataset*************************" % numlist)
    print(largest['Average CPU Time'])
    print(
        "**********************Top %s rows with most node average cpu time from merged dataset*************************" % numlist)
    print(largest)
    largest.to_csv(r'%s/topnodeaveragecputimejoined.csv' % outdir, index=False, header=True)

    # Total average cpu Time for flow from merged data
    flargest = df_join.nlargest(int(numlist), ['Average CPU Time_flow'])
    print("**********************Top %s flow average cpu time from merged dataset*************************" % numlist)
    print(flargest['Average CPU Time_flow'])
    print(
        "**********************Top %s rows with most flow average cpu time from merged dataset*************************" % numlist)
    print(flargest)
    flargest.to_csv(r'%s/topflowaveragecputimejoined.csv' % outdir, index=False, header=True)

    # Aeverage CPU Time for flow from flow data only
    flargest = df_flow.nlargest(int(numlist), ['Average CPU Time'])
    print("**********************Top %s highest average cpu time from flow dataset*************************" % numlist)
    print(flargest['Average CPU Time'])
    print(
        "**********************Top %s rows with flow average cpu time from flow dataset*************************" % numlist)
    print(flargest)
    flargest.to_csv(r'%s/topflowaveragecputimeflow.csv' % outdir, index=False, header=True)

    # Average CPU Time for node from node data only
    largest = df_node.nlargest(int(numlist), ['Average CPU Time'])
    print("**********************Top %s node average cpu time from node dataset*************************" % numlist)
    print(largest['Average CPU Time'])
    print(
        "**********************Top %s rows with highest average cpu time from node dataset*************************" % numlist)
    print(largest)
    largest.to_csv(r'%s/topnodeaveragecputimenode.csv' % outdir, index=False, header=True)

    # flow wise grouped data
    if showgroupeddata == 'yes':
        grouped = df_join.groupby(
            ['Message Flow Name', 'Broker Name', 'EG Name', 'EndTimeStampLambda', 'StartTimeStampLambda', 'Node Name',
             'Node Type'])
        print(grouped.first())

'''
if __name__ == "__main__":
    main(sys.argv[1:])
'''
