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
    doc: "The BAM file used as input."
    Format: "http://edamontology.org/format_2572" 
    inputBinding:
      prefix: -b

  klist_input:
    type: File
    doc: "A file with the list of khmer to consider."
    inputBinding:
      prefix: -k

  rf_input:
    type: File
    doc: "The trained Random Forest classifier."
    inputBinding:
      prefix: -rf

  chunk_size:
    type: int
    default: 10000
    doc: "The number of reads to analyze in a chunk."
    inputBinding:
      prefix: -s

outputs:
  ktag_output:
    type: File
    outputBinding:
      glob: ktag_output.tsv
    doc: "A file with the tag for each read (with at least one khmer present)."

baseCommand: ["python", "/usr/local/bin/ktag.py"]
