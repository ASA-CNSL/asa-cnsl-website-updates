from importlib import resources
import pathlib
import textwrap
from typing import Callable

import markdown

DEFAULT_OUTPUT_PATH = "generated/"

DEFAULT_TABLES = {
    "current-officers.md": "Current Officers",
    "chair.md": "Chair",
    "secretary-treasurer.md": "Secretary-Treasurer",
    "program-chair.md": "Program Chair",
    "publication-officer.md": "Publication Officer",
    "webmaster.md": "Webmaster",
    "communications-officer.md": "Newsletter Editor/Communications Officer",
    "section-council-representative.md": "Section Council Representative",
    "at-large-committee-member.md": "At-Large Committee Member",
    "student-liaison.md": "Student Liaison",
    "asa-liaison.md": "ASA Liaison",
}

class UtilRegistry:
    def __init__(self):
        self.registry: dict[str, Callable[[],None]] = {}

    @classmethod
    def register(cls):
        pass


def generate_officer_html(output_directory: str = None, tables: dict[str, str] = None):
    # Resolve the output directory.
    output_path = pathlib.Path(output_directory if output_directory is not None else DEFAULT_OUTPUT_PATH).joinpath("officers").resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Resolve the tables
    tables = tables if tables is not None else DEFAULT_TABLES

    # Load stylesheet.
    stylesheet = resources.files("asa-cnsl-utils").joinpath("resources/style", "table_style.css").read_text()

    style_html = f"""
    <!-- 
        NOTE TO FUTURE WEBMASTERS:
         This table HTML was generated using the script located at: https://github.com/ASA-CNSL/asa-cnsl-website-updates
         Please keep the source markdown files up-to-date, and generate the HTML using the provided script rather than
         updating this HTML by hand.
    -->
    <!-- BEGIN STYLESHEET -->\
    <style>
    {stylesheet}
    </style>
    <!-- END STYLESHEET -->
    """.strip("\n\t ")

    # Process markdown into HTML
    combined_table_html = style_html
    for table, table_heading in tables.items():
        # Read the markdown file
        table_text = resources.files("asa-cnsl-utils").joinpath("resources/officers").joinpath(table).read_text()
        # Convert to HTML
        table_tname = table.removesuffix(".md").upper()
        table_html = f"""
        <!-- BEGIN {table_tname} -->
        {markdown.markdown(table_text, extensions=["tables", "attr_list"])}
        <!-- END {table_tname} -->
        """.strip("\n\t ")
        # Add the stylesheet
        styled_table_html = style_html + "\n" + table_html
        # Write the individual table to file
        output_path.joinpath(table).with_suffix(".html").write_text(styled_table_html)
        # Add the table HTML to the combined output (except for current officers)
        if table != "current-officers.md":
            combined_table_html += "\n" + f"<h3>{table_heading}</h3>" + table_html

    # Write a combined table
    output_path.joinpath("tables_combined_ordered.html").write_text(combined_table_html)


if __name__ == "__main__":
    generate_officer_html()
