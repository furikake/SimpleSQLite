#!/usr/bin/env python
# encoding: utf-8


from simplesqlite import SimpleSQLite
import six


file_path = "sample_data_single.json"

# create sample data file ---
with open(file_path, "w") as f:
    f.write("""[
        {"attr_b": 4, "attr_c": "a", "attr_a": 1},
        {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
        {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
    ]""")

# create table ---
con = SimpleSQLite("sample.sqlite", "w")
con.create_table_from_json(file_path)

# output ---
for table_name in con.get_table_name_list():
    six.print_("table: " + table_name)
    six.print_(con.get_attribute_name_list(table_name))
    result = con.select(select="*", table_name=table_name)
    for record in result.fetchall():
        six.print_(record)
    six.print_()
