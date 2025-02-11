# TODO add a stylesheet
# TODO add ERD

import duckdb as db
import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class TableMetadata:
    name: str
    columns: list
    constraints: list

db_name = 'bordeaux.db'
db_path = Path.cwd() / 'bordeaux' / db_name

# metadata query creates temp tables from which to reference data
metadata_query = Path.cwd() / 'bordeaux' / 'db_docs.sql'

TABLE_NAMES = 'table_names'
COLUMNS = 'columns'
CONSTRAINTS = 'constraints'
database_name = ""

with db.connect(str(db_path), read_only=True) as conn:
    
    database_name = conn.execute("select database_name from duckdb_databases")fetch()[0]
    with open(metadata_query, 'r') as f:
        query = f.read()
        conn.execute(query)
        
    # first get the table names then generate container with the 
    # metadata for each.
    table_names = [x[0] for x in conn.execute(f"select table_name from {TABLE_NAMES}").fetchall()]
    
    tbl_mta = []
    for name in table_names:
        col_mta = conn.execute(f"select * from columns where table_name = '{name}'").df()
        constrt_mta = conn.execute(f"select * from constraints where table_name = '{name}'").df()
        
        tbl_mta.append(TableMetadata(name = name, columns=col_mta, constraints=constrt_mta))
        
# now we have the metadata, time to prepare the document

document = ""

for mta in tbl_mta:
    document += f"# {database_name}\n\n"
    document += f"## {mta.name}\n\n"
    document += f"### Columns\n\n"
    document += f"{mta.columns.to_html()}\n\n"
    document += f"### Constraints\n\n"
    document += f"{mta.constraints.to_html()}\n\n"
    
from markdown import markdown
import webbrowser

html = markdown(document)
html_path = Path.cwd() / "docs.html"
html_path.write_text(html)

import webbrowser
# see <https://unix.stackexchange.com/questions/99458/how-can-i-find-out-where-the-firefox-bin-is>
# for using firefox with webbrowser
firefox = webbrowser.Mozilla("/Applications/Firefox.app/Contents/MacOS/firefox")
firefox.open(str(html_path), 0)

# cleanup

# webbrowser open needs a slight delay to open the file
from time import sleep
sleep(0.5)
html_path.unlink()