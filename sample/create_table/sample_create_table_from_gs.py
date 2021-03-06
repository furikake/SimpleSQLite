#!/usr/bin/env python
# encoding: utf-8


import simplesqlite
import six


credentials_file = "sample-xxxxxxxxxxxx.json"

# create table ---
con = simplesqlite.SimpleSQLite("sample.sqlite", "w")

loader = simplesqlite.loader.GoogleSheetsTableLoader(credentials_file)
loader.title = "samplebook"

for tabledata in loader.load():
    con.create_table_from_tabledata(tabledata)

# output ---
for table_name in con.get_table_name_list():
    six.print_("table: " + table_name)
    six.print_(con.get_attribute_name_list(table_name))
    result = con.select(select="*", table_name=table_name)
    for record in result.fetchall():
        six.print_(record)
    six.print_()
