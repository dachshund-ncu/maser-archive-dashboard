from database_handler.archive_handler import move_files_to_database
from maser_archive import ARCHIVE_DIR, SOURCES_DB, TARED_DIR
import streamlit as st
import os
from PIL import Image
DE_CAT = os.path.dirname(__file__)

def main():
    st.set_page_config(page_title="Torun 6.7 GHz methanol maser archive")

    uploaded_files = st.file_uploader("Upload .fits files", accept_multiple_files=True, type=['fits'])
   
    if uploaded_files is not None:
        # upload sources to the database
        sources = move_files_to_database(uploaded_files, ARCHIVE_DIR, SOURCES_DB)
        # generate tarball
        os.chdir(ARCHIVE_DIR)
        for src in sources:
            os.system(f"tar -cvjf {os.path.join(TARED_DIR, src + '.tar.bz2')} {src}")
        os.chdir(DE_CAT)
if __name__ == '__main__':
    main()