import sys
from optparse import OptionParser
import logging
from cassis import *
import csv

# create a option parser instance, allowing us to specify custom options. We create a option '-o --output' to enable
# the user to choose their preferred output filename.
parser = OptionParser()
parser.add_option("-o", "--output", dest="filename",default="", action="store", type="string",
                  help="The putput file", metavar="filename")

# read the options from stdin
(options, args) = parser.parse_args()

# accumulate the xmi from stdin into a string
xmi_representation = ""
for line in sys.stdin:
    xmi_representation += line

# create CAS from xmi and typesystem
with open('sample_typesystem.xml', 'rb') as f:
    sample_typesystem = load_typesystem(f)

merged_typesystem = merge_typesystems(sample_typesystem, load_dkpro_core_typesystem())
cas = load_cas_from_xmi(xmi_representation, typesystem=merged_typesystem)

# write tokens of CAS into a csv file.
with open(options.filename, 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for token in cas.select('de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity'):
        writer.writerow([cas.sofa_string[int(token.begin):int(token.end)], token.begin, token.end, token.value])


