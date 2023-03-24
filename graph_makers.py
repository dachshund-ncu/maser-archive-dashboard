import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from radio_toolbox.fits_readers import setOfSpec
import pandas as pd
import streamlit as st

def make_light_curve_channel(df: pd.DataFrame):
    '''
    Makes light curve plotly graph: integrated
    '''
    fig = px.line(df, x='MJD', y=["I", "V", "LHC", "RHC"],
                  labels={
                    "MJD": "MJD",
                    "value": "Flux density (Jy)"
                  }, markers=True)
    return fig

def make_light_curve_integrated(df: pd.DataFrame):
    '''
    Makes light curve plotly graph: integrated
    '''
    fig = px.line(df, x='MJD', y=["I", "V", "LHC", "RHC"],
                  labels={
                    "MJD": "MJD",
                    "value": "Integrated flux density (Jy / km / s)"
                  }, markers=True)
    return fig

def make_spectrum(df: pd.DataFrame, velocity: float):
    '''
    Makes single-spectrum plotly graph
    '''
    fig = px.line(df, x='Velocity', y=["I", "V", "LHC", "RHC"],
                  labels={
                    "Velocity": "Velocity (km/s)",
                    "value": "Flux density (Jy)"
                  })
    fig.add_vline(velocity, line_dash='dash', line_color="green")
    return fig

def make_heatmap(x: np.ndarray, y: np.ndarray, z: np.ndarray, rms: float, log_scale: bool):
    '''
    Returns a heatmap for the given dataset
    '''
    if log_scale:
      indices = z < 3.0 * rms
      z[indices] = 3.0 * rms
      z = np.log(z)
      hover_template = "MJD: %{x:.2f}<br>Velocity (km/s): %{y:.2f}<br>Flux density (log(Jy)): %{z:.2f}"
    else:
      hover_template = "MJD: %{x:.2f}<br>Velocity (km/s): %{y:.2f}<br>Flux density (Jy): %{z:.2f}"
    fig = go.Figure(data=go.Heatmap( z = z, x = x, y = y, colorscale='jet', hovertemplate=hover_template))
    return fig