# Copyright 2022 IBM Corporation 
# Author: Amar Shah
 
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the MIT License
#  which accompanies this distribution, and is available at
#  http://opensource.org/licenses/MIT
 
#  Contributors:
#      Amar Shah, Hina Sharma,  Anshu Garg


import plotly
from plotly.subplots import make_subplots

plotly.__version__
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, json
import pandas as pd
import appconnect_analytics_updated as appc
import plotly.express as px
import plotly.graph_objs as go
from IPython.display import HTML




app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart1')
def chart1():

    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df_msgelaps, df_msgcpu=appc.flask_elapsed_graph(created_df,msgFlowcnt)
    header = "Message Flow vs Avg. Elapsed Time and CPU Time"
    description = """
            The above graphs give the analysis of the message flows 
            consuming the highest avg. elapsed time and cpu time."""
    df=df_msgelaps
    df1=df_msgcpu
    return render_template('notdash2.html',
                           tables=[df.to_html(classes='elapse'),df1.to_html(classes='cpumess')],
                           titles=['na','Elapsed Time ',
                                   'CPU Time'])

@app.route('/chart2')
def chart2():
    df_input=pd.DataFrame()
    df_top=pd.DataFrame()
    df_top = appc.allrecords_topmsgflow_elapsed(created_df, msgFlowcnt)
    #print("df_top",df_top.columns)
    fig=appc.msg_input_vs_elapsedtime(created_df,df_top,msgFlowcnt)
    header = "Input Message Flows vs Elapsed Time"
    description = """
                The  graphs provide the analysis of input message flow vs 
                Average Elapsed Time"""
    #plt.savefig(fig)
    # fig=px.line(x=df_input['Total Number of Input '
    #                                             'Messages'], y=df_input[
    #     'Average Elapsed Time_flow'])

    #fig = px.bar(df, x=”Fruit”, y =”Amount”, color =”City”, barmode =”group”)
    # graphJSON = json.dumps(HTML(fig.to_html()),
    #                        cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('inputgraph.html',graphJSON=HTML(fig.to_html()),header=header,
                           description=description)


@app.route('/chart3')
def chart3():
    df_top=appc.allrecords_topmsgflow_elapsed(created_df, msgFlowcnt)

    appc.msg_heatmap_hourly(created_df,df_top,msgFlowcnt)
    header="HeatMaps"
    description = """
    Heatmaps giving the description of the hourly variations in Average 
    Elapsed Time 
    for 
    the Message Flows causing performance deviations.
    """
    return render_template('upload.html',
                           header=header,description=description)

if __name__ == '__main__':
    created_df=appc.main(appc.sys.argv[1:])
    msgFlowcnt=appc.msgflwcnt(created_df)
    app.run()


