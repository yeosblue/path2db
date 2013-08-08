#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import sys
import os
from mosql.common import insert

DB_USER = ''
DB_PSWD = ''
DB_NAME = ''

def list_files_in(directory, verbose=True):
    path_list = []
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for f in file_names:
	    rel_path = os.path.relpath(dir_path, root_dir)
	    file_path = '/' + os.path.join(rel_path, f)
	    path_list.append(file_path)
	    if verbose:
	        print file_path
    if verbose:
        print
    return path_list

def confirm(statement):
    yes = set(['yes', 'y', 'ok', 'sure'])
    no = set(['no', 'n'])
    choice = raw_input(statement).strip().lower()
    if choice in yes:
    	return True
    elif choice in no:
	return False
    else:
        raise ValueError

def import_to_db(db, path_list):
    cur = db.cursor()
    images_creating_sql = insert('tagging_images', 
		 		columns=('img_path'),
				values=[(path,) for path in path_list])
    cur.execute(images_creating_sql)
    db.commit()

if __name__ == '__main__':

    root_dir = '.'
    if len(sys.argv) > 1:
	root_dir = sys.argv[1]
	print
    else:
	print 'Root directory is undefined'
	exit()

    paths = list_files_in(root_dir)
    try:
	if confirm(' >> Do you want to import into db? '):

	    db = MySQLdb.connect(
				host='localhost',
			 	user=DB_USER,
			 	passwd=DB_PSWD,
			 	db=DB_NAME)
	    print ' >> Start importing '
	    import_to_db(db, paths)
	    print ' >> Finished '
	else:
	    print ' >> Fine. I will not import anything.'
    except ValueError:
	print ' >> I can\'t understand what you said'
    except:
	raise
