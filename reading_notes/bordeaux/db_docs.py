# TODO add a stylesheet
# TODO add ERD

import duckdb as db
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
    
    database_name = conn.execute("select database_name from duckdb_databases").fetchone()[0]
    with open(metadata_query, 'r') as f:
        query = f.read()
        conn.execute(query)
        
    # first get the table names then generate container with the 
    # metadata for each.
    table_names = [x[0] for x in conn.execute(f"select table_name from {TABLE_NAMES}").fetchall()]
    
    tbl_mta = []
    for name in table_names:
        col_mta = conn.execute(f"select column_name, comment, column_default, is_nullable, datatype from columns where table_name = '{name}'").df()
        constrt_mta = conn.execute(f"select constraint_text, constraint_column_names from constraints where table_name = '{name}'").df()
        
        tbl_mta.append(TableMetadata(name = name, columns=col_mta, constraints=constrt_mta))
        
# now we have the metadata, time to prepare the document
css_path = Path.cwd() / 'css.css'
document = ""
document += "<html>\n"
document += "<head>\n"
document += f"   <link rel=\"stylesheet\" href=\"{css_path}\">\n"
document += f"<title>{database_name}</title>"
document += "</head>\n"

document += f"<h1>Database: {database_name}</h1>"

for mta in tbl_mta:
    document += f"<h2>Table: {mta.name}</h2>"
    document += "<br>"
    document += f"<h3>Columns</h3>"
    document += "<br>"
    document += f"{mta.columns.to_html()}\n\n"
    document += "<br>"
    document += "<br>"
    document += "<h3>Constraints</h3>"
    document += "<br>"
    document += f"{mta.constraints.to_html()}\n\n"
    document += "<br>"
    document += "<br>"
    
document += "</body>"
document += "</html>"

from markdown import markdown
import webbrowser
import html

html_str = markdown(document)

html_path = Path.cwd() / "docs.html"
html_path.write_text(html_str)

import webbrowser
# see <https://unix.stackexchange.com/questions/99458/how-can-i-find-out-where-the-firefox-bin-is>
# for using firefox with webbrowser
firefox = webbrowser.Mozilla("/Applications/Firefox.app/Contents/MacOS/firefox")
firefox.open(str(html_path), 0)

# cleanup

# webbrowser open needs a slight delay to open the file
# from time import sleep
# sleep(0.5)
# html_path.unlink()