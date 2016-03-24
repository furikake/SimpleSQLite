# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


from __future__ import absolute_import
import logging
import os
import re
import sys
import sqlite3

import dataproperty

from .core import SimpleSQLite


MEMORY_DB_NAME = ":memory:"
__INVALID_PATH_CHAR = '\:*?"<>|'


def validate_file_path(file_path):
    """
    :param str file_path: File path to validate.
    :raises ValueError:
        If ``file_path`` is empty or include invalid char (``\:*?"<>|``).
    """

    if dataproperty.is_empty_string(file_path):
        raise ValueError("path is null")

    if file_path == MEMORY_DB_NAME:
        return

    match = re.search("[%s]" % (
        re.escape(__INVALID_PATH_CHAR)), os.path.basename(file_path))
    if match is not None:
        raise ValueError(
            "invalid char found in file name: '%s'" % (
                re.escape(match.group())))


def validate_table_name(name):
    """
    :param str name: Table name to validate.
    :raises ValueError: If ``name`` is empty.
    """

    if dataproperty.is_empty_string(name):
        raise ValueError("table name is empty")


def append_table(con_src, con_dst, table_name):
    """
    :param SimpleSQLite con_src: Copy source database.
    :param SimpleSQLite con_dst: Copy destination database.
    :param str table_name: Table name to copy.

    :return: Part of WHERE query of SQLite.
    :rtype: bool

    .. seealso::

        :py:meth:`simplesqlite.core.SimpleSQLite.verify_table_existence`
        :py:meth:`simplesqlite.core.SimpleSQLite.create_table_with_data`
    """

    con_src.verify_table_existence(table_name)
    con_dst.validate_access_permission(["w", "a"])

    if con_dst.has_table(table_name):
        src_attr_list = con_src.get_attribute_name_list(table_name)
        dst_attr_list = con_dst.get_attribute_name_list(table_name)
        if src_attr_list != dst_attr_list:
            raise ValueError("""
            source and destination attribute is different from each other
              src: %s
              dst: %s
            """ % (str(src_attr_list), str(dst_attr_list)))

    result = con_src.select(select="*", table_name=table_name)
    if result is None:
        return False
    value_matrix = result.fetchall()

    con_dst.create_table_with_data(
        table_name,
        con_src.get_attribute_name_list(table_name),
        value_matrix)

    return True


# class ---

class NullDatabaseConnectionError(Exception):
    pass


class TableNotFoundError(Exception):
    pass


class AttributeNotFoundError(Exception):
    pass


def connect_sqlite_db_mem():
    """
    :return: Instance of a in memory database
    :rtype: SimpleSQLite
    """

    return SimpleSQLite(MEMORY_DB_NAME, "w")
