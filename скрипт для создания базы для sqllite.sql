CREATE TABLE reports (id_reports INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, html_xsl BLOB, excel_xsl BLOB, word_xsl BLOB, proc_name TEXT, field_sort TEXT);

CREATE TABLE fields_report (id_field INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_report INTEGER REFERENCES reports (id_reports) NOT NULL, name TEXT, type TEXT, label TEXT);

CREATE TABLE fields_collection (id_field_collection INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_field INTEGER REFERENCES fields_report (id_field) NOT NULL, value TEXT, label TEXT);