#!/usr/bin/env cwl-runner
  
class: CommandLineTool
id: "Ktag"
label: "Ktag tool"
cwlVersion: v1.0 
doc: |
    ![build_status](https://quay.io/repository/jmonlong/dockstore-ktag/status)
    A Docker container for the Ktag command. 

dct:creator:
  "@id": "http://orcid.org/0000-0002-9737-5516"
  foaf:name: Jean Monlong
  foaf:mbox: "mailto:jean.monlong@mail.mcgill.ca"
  
requirements:
  - class: DockerRequirement
    dockerPull: "quay.io/jmonlong/dockstore-ktag"

hints:
  - class: ResourceRequirement 
    coresMin: 1
    ramMin: 4092  # "the process requires at least 4G of RAM"
    outdirMin: 512000

inputs:
  bam_input:
    type: File
    doc: "The BAM file used as input, it must be indexed."
    format: "http://edamontology.org/format_2572" 
    inputBinding:
      prefix: -b

  kilst_input:
    type: File
    doc: "A file with the list of khmer to consider."
    inputBinding:
      prefix: -k

outputs:
  ktag_output:
    type: File
    outputBinding:
      prefix: -o
    doc: "A file with the tag for each read (with at least one khmer present)."

baseCommand: ["bash", "/usr/local/bin/ktag.py"]
