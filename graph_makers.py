import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from radio_toolbox.fits_readers import setOfSpec
import pandas as pd

def make_light_curve(df: pd.DataFrame):
    '''
    Makes single-spectrum plotly graph
    '''
    fig = px.line(df, x='MJD', y=["I", "V", "LHC", "RHC"],
                  labels={
                    "MJD": "MJD",
                    "value": "Integrated flux density (Jy / km / s)"
                  }, markers=True)
    return fig

def make_spectrum(df: pd.DataFrame):
    '''
    Makes single-spectrum plotly graph
    '''
    fig = px.line(df, x='Velocity', y=["I", "V", "LHC", "RHC"],
                  labels={
                    "Velocity": "Velocity (km/s)",
                    "value": "Flux density (Jy)"
                  })
    return fig

def make_heatmap(data: setOfSpec):
    x = data.getMjdArray()
    y = data.getVelArray()
    z = data.get2DdataArray(pol='I')
    indices = z < 0.01
    z[indices] = 0.01
    fig = go.Figure(data=go.Heatmap(
                        z = z,
                        x = x, 
                        y = y,
                        colorscale='jet'))
    
    # fig.update_layout({'plot_bgcolor': "#21201f", 'paper_bgcolor': "#21201f", 'legend_orientation': "h"},
    #               legend=dict(y=1, x=0),
    #               font=dict(color='#dedddc'), dragmode='pan', hovermode='x unified',
    #               margin=dict(b=20, t=0, l=0, r=40))
    # fig.update_xaxes(showgrid=False, zeroline=False, rangeslider_visible=False, showticklabels=False, showspikes=True, spikemode='across', spikesnap='data', showline=False, spikedash='dash')
    # fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, showspikes=True, spikemode='across', spikesnap='data', showline=False, spikedash='dash')
    
    
    return fig