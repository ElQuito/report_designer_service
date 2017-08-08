CREATE TABLE reports (id_reports INTEGER NOT NULL IDENTITY(1,1) PRIMARY KEY, name TEXT, html_xsl varchar(max), excel_xsl varchar(max), word_xsl varchar(max), proc_name TEXT, field_sort TEXT);

CREATE TABLE fields_report (id_field INTEGER NOT NULL IDENTITY(1,1) PRIMARY KEY, id_report INTEGER REFERENCES reports (id_reports) NOT NULL, name TEXT, type TEXT, label TEXT);

CREATE TABLE fields_collection (id_field_collection INTEGER NOT NULL IDENTITY(1,1) PRIMARY KEY, id_field INTEGER REFERENCES fields_report (id_field) NOT NULL, value TEXT, label TEXT);