# Maser archive dashboard
This is a maser archive dashboard. Written using streamlit framework
## Target platform
Gnu/Linux
## Requirements
App is tested under git version 2.34.1 and python 3.10.
Python 3.8 and newer should be fine (but it is not guaranteed).
## Setting up the repository
```bash
git clone https://github.com/dachshund-ncu/maser-archive-dashboard.git
git submodule init
git submodule update
```
## Installing depedencies
```bash
sudo apt install libbz2-dev
sudo apt install gfortran
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Runing the archive
### Dashboard
```bash
streamlit run maser_archive.py
```
### Uploader
```bash
streamlit run maser_uploader.py
```

# Dashboard working flowchart
```mermaid
flowchart TD

archive_main[Archive main directory] --> sources
sources --> source_1[Source 1] --> m_band[m_band directory] --> fits_files[.fits files]
sources --> source_2[Source 2] --> m_band2[m_band directory] --> fits_files2[.fits files]
sources --> source_3[...]

archive_main --> maser_observations_db[(Maser observations database)]

subgraph files_place[Archive]
archive_main
sources
source_1
source_2
source_3
m_band
m_band2
fits_files
fits_files2
maser_observations_db
end

dashboard((Maser archive dashboard))


database_handler(Database handler) -- source parameters -->  dashboard 

maser_observations_db -- source parameters --> database_handler
fits_files2 -- data for graphs --> dashboard

uploader((Maser archive uploader))
uploader -- update database and files --> database_handler -- updated info --> maser_observations_db
database_handler -- add new files --> fits_files2
subgraph services[Services]
dashboard
uploader
end
```