"""Python interface to GenoLogics LIMS via its REST API.
    
    Usage example: set_udf_size.py user password processURI 
    
    Works with output files from 'Bioanalyzer QC (DNA) 4.0' Process.
    Set UDF 'Size (bp)' by copying the value from 'Region 1 Average Size - bp'
    
    
    
    Daria Goranskaya, Science for Life Laboratory, Stockholm, Sweden.
    """

from pprint import pprint
from genologics.lims import *
import sys

def get_process_output_files(Process):
    result=[]
    for input, output in process.input_output_maps:
        if output:
            if(output['output-type']=='ResultFile'):
                result.append(output['uri'])
    #result #[Artifact(Artifact(92-44009)), Artifact(Artifact(92-44010))]
    return result

def modify_artifact(process):
    result=get_process_output_files(process)
    #artifact=result[0]
    for artifact in result:
        #print artifact.name, 'Size (bp)',  artifact.udf['Size (bp)'], 'Region 1 Average Size - bp', artifact.udf['Region 1 Average Size - bp']
        artifact.udf['Size (bp)']=artifact.udf['Region 1 Average Size - bp']
        artifact.put()


# Login parameters for connecting to a LIMS instance.
#from genologics.config import BASEURI, USERNAME, PASSWORD=sys.arg
BASEURI='https://genologics-stage.scilifelab.se:8443'
USERNAME=sys.argv[1]
PASSWORD=sys.argv[2]
processURI=sys.argv[3]

#print 'Argument List:', str(sys.argv)
# Create the LIMS interface instance, and check the connection and version.
lims = Lims(BASEURI, USERNAME, PASSWORD)
lims.check_version()


process=Process(lims,uri=processURI)

modify_artifact(process)

#Add logging info?