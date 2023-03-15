#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from radio_toolbox.fits_readers import Spectrum, setOfSpec
import glob
import matplotlib.pyplot as plt
import plotly
from graph_makers import make_heatmap, make_spectrum, make_light_curve



ARCHIVE_DIR = '/home/michu/Drop/Dropbox/metvar_archive/fits_sources'
ARCHIVE_SUBDIR = 'm_band'
DE_CAT = os.path.dirname(__file__)
LOADED_DATA = None

def read_sources_from_archive(directory: str) -> list:
    '''
    Reads the list of sources from archive
    '''
    table = []
    for root, dir, file in os.walk(directory, topdown=True):
        for d in dir:
            if not d.endswith("_band"):
                table.append(d)
    return sort_sources(table)

def sort_sources(list_with_sources: list) -> list:
    '''
    Bubble-sorts the sources based on their galactic longitude 
    '''
    longitudes = get_gal_longi(list_with_sources)
    return [item for l, item in sorted(zip(longitudes, list_with_sources))]

def get_gal_longi(list_with_sources: str) -> list:
    '''
    returns the list of galactic longitudes
    '''
    longitudes = []
    for item in list_with_sources:
        # split
        tmp = item.split('+')
        if len(tmp) < 2:
            tmp = item.split('-')
        # float
        longitudes.append(float(tmp[0]))
    return longitudes

def on_click(*args, **kwargs):
    '''
    Invoked when sidebar button is clicked
    Aims to display dta on the central panel
    '''
    st.title(args[0])
    with st.spinner(f"Loading {args[0]}"):
        data = load_spectral_data(args[0])

    # -- Heat map --
    st.subheader("Heat map plot")
    st.plotly_chart(make_heatmap(data), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mean spectrum")
        st.plotly_chart(make_spectrum(data.get_mean_spectrum()))
    with col2:
        st.subheader("Integrated flux density")
        st.plotly_chart(make_light_curve(data.get_integrated_flux_density(500, 1500, df=True)))

def load_spectral_data(sourcename: str) -> setOfSpec:
    '''
    Loads data from the .fits files of a given source
    '''
    # get the list of .fits files
    return setOfSpec(os.path.join(ARCHIVE_DIR, sourcename, ARCHIVE_SUBDIR))


def main():
    im = Image.open(os.path.join(DE_CAT, 'assets', 'dachshund_of_doom_logo_no_sign_inkscape.png'))
    st.set_page_config(page_title="Torun 6.7 GHz methanol maser archive", layout='wide', page_icon=im)
    list_of_sources = read_sources_from_archive(ARCHIVE_DIR)

    with st.sidebar:
        st.sidebar.title("Sources")
        for source in list_of_sources:
            st.button(source, use_container_width=True, on_click = on_click, args=[source])
    
    
if __name__ == '__main__':
    main()