#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import streamlit as st
import numpy as np
import os
import pandas as pd
from radio_toolbox.fits_readers import setOfSpec
from graph_makers import make_heatmap, make_spectrum, make_light_curve_integrated, make_light_curve_channel
from database_handler.db_handler import sources_database

# DE_CAT = os.path.dirname(__file__)
# ARCHIVE_DIR = os.path.join(DE_CAT, 'archive')
# ARCHIVE_SUBDIR = 'm_band'
# TARED_DIR = os.path.join(DE_CAT, 'tared_archives', 'fits_to_send')
# SOURCES_DB = sources_database(os.path.join(DE_CAT, 'archive', 'maser_database.db'))

DE_CAT = os.path.dirname(__file__)
ARCHIVE_DIR = '/home/michu/Drop/Dropbox/metvar_archive/fits_sources'
ARCHIVE_SUBDIR = 'm_band'
TARED_DIR = '/home/michu/Drop/Dropbox/metvar_archive/tarer/fits_to_send'
SOURCES_DB = sources_database(os.path.join(os.path.dirname(ARCHIVE_DIR), 'maser_archive_db.db'))

def read_sources_from_database(db: sources_database) -> list:
    '''
    Reads list of sourcenames from the database file:
    Arguments:
        |   db: sources_database object with database loaded
    Returns:
        |   sources_l: list with sourcenames
    '''
    return [row[1] for row in db.get_all_sources()]

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

def on_click(data: setOfSpec, log_scale: bool, velocity_for_lc: float, source_metadata: tuple):
    '''
    Invoked when sidebar button is clicked
    Aims to display dta on the central panel
    '''

    # prepare the data
    x = data.getMjdArray()
    y = data.getVelArray()
    z = data.get2DdataArray(pol='I')
    rms = np.mean([sp.rmsIhc for sp in data.spectra])
    # light curve
    lcs_df, vel_of_chan = data.get_light_curve(velocity_for_lc, df=True)
    # data preparation
    
    if source_metadata is not None:
        source_metadata.style.hide(axis="index")
        st.subheader("%s parameters" % (source_metadata["Value"][0]))
        st.dataframe(source_metadata, use_container_width=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Heat map plot")
        st.plotly_chart(make_heatmap(x,y,z,rms, log_scale = log_scale))
        st.subheader("Mean spectrum")
        st.plotly_chart(make_spectrum(data.get_mean_spectrum(), vel_of_chan))
    with col2:
        st.subheader("Integrated flux density")
        st.plotly_chart(make_light_curve_integrated(data.get_integrated_flux_density(0, len(data.spectra[0].velocityTable), df=True)))
        st.subheader(f"Light curve along {round(vel_of_chan,2)} km/s")
        st.plotly_chart(make_light_curve_channel(lcs_df))

def load_spectral_data(sourcename: str) -> setOfSpec:
    '''
    Loads data from the .fits files of a given source
    '''
    # get the list of .fits files
    return setOfSpec(os.path.join(ARCHIVE_DIR, sourcename, ARCHIVE_SUBDIR))


def main():
    '''
    Main method of the dashboard app
    '''
    im = Image.open(os.path.join(DE_CAT, 'assets', 'dachshund_of_doom_logo_no_sign_inkscape.png'))
    st.set_page_config(page_title="Torun 6.7 GHz methanol maser archive", layout='wide', page_icon=im)

    # get the list of sources for the archive
    # list_of_sources = read_sources_from_archive(ARCHIVE_DIR)
    list_of_sources = read_sources_from_database(SOURCES_DB)

    # get the sidebar rollin'
    with st.sidebar:
        st.sidebar.title("Select source")
        option = st.selectbox("select source", [source for source in list_of_sources], label_visibility="collapsed")
        with st.form("Form"):
            if option is not None and option != "":
                with st.spinner(f"Loading {option}"):
                    data = load_spectral_data(option)
            st.title(option)
            source_metadata = SOURCES_DB.get_source_df(option)
            log_scale = st.checkbox("Heatmap log-scale", value=False)
            mjds = data.getMjdArray()
            vels = data.getVelArray()
            dv = abs(vels[1] - vels[0])
            epoch_range = st.slider("Epoch span", float(mjds.min() - 1), float(mjds.max() + 1), (float(mjds.min()), float(mjds.max())) ) 
            channel_range = st.slider("Velocity span", float(vels.min() - dv), float(vels.max() + dv), ( float(vels.min() - dv), float(vels.max() + dv) ) )
            vel_for_lc = st.slider("Light curve at the velocity:", *channel_range)
            submit = st.form_submit_button("Submit", use_container_width=True)
        with open(os.path.join(TARED_DIR, str(option)+'.tar.bz2'), 'rb') as file_archive:
            st.download_button("Download .fits files", file_archive, str(option)+'.tar.bz2', use_container_width=True)
    
    # after the submit - proceed with updating the dashboard contents
    if submit:
        ss = data.make_slice(channel_range, epoch_range)
        on_click(ss, log_scale, vel_for_lc, source_metadata)


if __name__ == '__main__':
    main()