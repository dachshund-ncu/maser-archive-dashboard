import sqlite3
from sqlite3 import Error
import os
import pandas as pd

DE_CAT = os.path.dirname(__file__)

class sources_database:
    def __init__(self, db_file: str):
        self.database_file = db_file
    
    def __create_connection(self) -> sqlite3.Connection:
        '''
        Connects to the database
        '''
        conn = None
        try:
            conn = sqlite3.connect(self.database_file)
        except Error as e:
            print(e)
        return conn

    def create_table(self, table_name: str):
        '''
        Creates the table for the statement, given in the argument
        '''
        try:
            conn = self.__create_connection()
            c = conn.cursor()
            command = "CREATE TABLE IF NOT EXISTS sources (id integer PRIMARY KEY, name text NOT NULL, ra text, dec text, v_lsr real)"
            c.execute(command)
            conn.close()
        except Error as e:
            print(e)

    def add_source(self, data_tuple: tuple):
        '''
        Adds source to the database - based on the tuple
        '''
        conn = self.__create_connection()
        command = "INSERT INTO sources (name, ra, dec, v_lsr) VALUES (?,?,?,?)"
        cur = conn.cursor()
        cur.execute(command, data_tuple)
        conn.commit()
        conn.close()
        return cur.lastrowid

    def update_source(self, data_tuple: tuple):
        '''
        Updates source in the database
        '''
        try:
            # prepare data
            conn = self.__create_connection()
            id_number = self.get_id_from_name(data_tuple[0])
            target_data_tuple = (*data_tuple, id_number)

            # prepare command
            command = "UPDATE sources SET name = ?, ra = ?, dec = ?, v_lsr = ? WHERE id = ?"
            c = conn.cursor()
            c.execute(command, target_data_tuple)

            # commit to database & close
            conn.commit()
            conn.close()
        except Error as e:
            print(e)
    
    def delete_source(self, source_name: str):
        '''
        deletes the source from database
        '''
        conn = self.__create_connection()
        source_id = self.get_id_from_name(source_name)
        command = 'DELETE FROM sources WHERE id = ?'
        cur = conn.cursor()
        cur.execute(command, (source_id,))
        conn.commit()
        conn.close()

    def delete_all_sources(self):
        '''
        Deletes all of the sources from the database
        '''
        conn = self.__create_connection()
        sql = 'DELETE FROM sources'
        cur  = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
    
    def get_all_sources(self):
        '''
        Returns iterator with all sources
        '''
        conn = self.__create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sources")
        iterator = cur.fetchall()
        conn.close()
        return iterator

    def get_source(self, sourcename: str):
        '''
        returns the source by name
        '''
        conn = self.__create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sources WHERE name = ?", (sourcename,))
        selection = cur.fetchall()
        conn.close()
        if len(selection) > 0:
            return selection[0]
    
    def get_source_df(self, sourcename: str):
        '''
        returns the source disctionary
        '''
        params = ["Name", "RA", "DEC", "V_lsr"]
        src = self.get_source(sourcename)
        if src is not None:
            return pd.DataFrame(list(zip(params, src[1:])), columns=["Parameter", "Value"], index=None )
        
    def get_id_from_name(self, sourcename: str) -> int:
        '''
        Returns the id from sourcename
        '''
        src = self.get_source(sourcename)
        if src is not None:
            return self.get_source(sourcename)[0]
        
    def print(self):
        for row in self.get_all_sources():
            print(row)

if __name__ == '__main__':
    db = sources_database('maser_archive_database.db')
    ee = db.get_source_df('109.871+2.114')
    print(ee["Value"][0])