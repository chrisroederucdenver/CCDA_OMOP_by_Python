
"""
    CodeSnooper - looks for code elements, fetches their code and codeSystem
                  attributes, mapping OIDs to vocabularies and
                  concept codes to names, lists the paths to the elements
                  with their attributes.
"""

import argparse
import re   # https://docs.python.org/3.9/library/re.html
import xml.etree.ElementTree as ET  # https://docs.python.org/3/library/xml.etree.elementtree.html
import tools.util as TU
from util.xml_ns import ns
from util.vocab_map_file import oid_map
from util import spark_util
from util.vocab_spark import VocabSpark

INPUT_FILENAME = 'resources/CCDA_CCD_b1_InPatient_v2.xml'
spark_util_object = spark_util.SparkUtil()
spark = spark_util_object.get_spark()

parser = argparse.ArgumentParser(
    prog='CCDA - OMOP Code Snooper',
    description="finds all code elements and shows what concepts the represent",
    epilog='epilog?')
parser.add_argument('-f', '--filename', default=INPUT_FILENAME,
                    help="filename to parse")
args = parser.parse_args()

tree = ET.parse(INPUT_FILENAME)

for path in TU.pathGen(INPUT_FILENAME):
    # just get the paths that end with a code element (tag)
    if re.fullmatch(r".*/code", path):
        for code_element in tree.findall(path, ns):
            try:
                vocabulary_oid = code_element.attrib['codeSystem']
                vocabulary_id = oid_map[vocabulary_oid][0]
                concept_code = code_element.attrib['code']
                details = VocabSpark.lookup_omop_details(spark, vocabulary_id, concept_code)
                if details is not None:
                    concept_name = details[2]
                    domain_id = details[3]
                    class_id = details[4]
                    print((f"{path}  vocab:{vocabulary_id} code:{concept_code}"
                           " \"{concept_name}\" domain:{domain_id} class:{class_id}"))
                else:
                    print((f"{path}  vocab:{vocabulary_id} code:{concept_code} "
                          "(code not available in OMOP vocabulary here)"))
            except Exception:
                print((f"{path}  -- no attributes, or not both --"
                      f" oid:{vocabulary_oid}  code:{concept_code}"))
