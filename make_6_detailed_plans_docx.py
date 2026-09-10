# -*- coding: utf-8 -*-
import zipfile, io, os
from generate_car_docx import esc, make_p, make_callout, make_table

def make_page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

print("Preparing to generate 6 comprehensive lesson plans...")
