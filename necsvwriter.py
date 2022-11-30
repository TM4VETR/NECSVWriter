import sys
from optparse import OptionParser
import logging
from cassis import *
import csv

parser = OptionParser()
parser.add_option("-o", "--output", dest="filename",default="", action="store", type="string",
                  help="The putput file", metavar="filename")
args = parser.parse_args()

(options, args) = parser.parse_args()

c = ""
for line in sys.stdin:
    c = c + line

# Default Typesystem
typesystem=load_dkpro_core_typesystem()
# make cas out of stdin
cas = load_cas_from_xmi(c, typesystem=load_dkpro_core_typesystem())

with open(options.filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for token in cas.select('de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity'):
        writer.writerow ([cas.sofa_string[int(token.begin):int(token.end)], token.begin, token.end, token.value])


