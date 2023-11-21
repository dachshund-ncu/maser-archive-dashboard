from database_handler.archive_handler import move_files_to_database
from maser_archive import ARCHIVE_DIR, SOURCES_DB
import streamlit as st
from PIL import Image


def main():
    st.set_page_config(page_title="Torun 6.7 GHz methanol maser archive")

    uploaded_files = st.file_uploader("Upload .fits files", accept_multiple_files=True, type=['fits'])
   
    if uploaded_files is not None:
        move_files_to_database(uploaded_files, ARCHIVE_DIR, SOURCES_DB)
        
if __name__ == '__main__':
    main()