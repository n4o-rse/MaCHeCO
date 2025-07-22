import os
import sys
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal

def main():
    # Base directory (where this script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Main CIDOC CRM file in the base directory
    cidoc_file = os.path.join(base_dir, "CIDOC_CRM_v7.1.3.rdf")

    # Extensions located in the 'extensions' subdirectory
    extensions_dir = os.path.join(base_dir, "extensions")
    extension_files = [
        "AAAo_v2.0.rdf",
        "CRMarchaeo_v2.1.1.rdf",
        "CRMba_v1.4.rdf",
        "CRMdig_v3.2.1.rdf",
        "CRMgeo_v1.2.rdf",
        "CRMinf_v0.7.rdf",
        "CRMsci_v2.0.rdf",
        "CRMtex_v2.0.rdf"
    ]

    # File format of the RDF sources (RDF/XML)
    source_format = "xml"

    # Namespaces
    DCTERMS = Namespace("http://purl.org/dc/terms/")

    # Create a new rdflib Graph object to hold all triples
    combined_graph = Graph()
    combined_graph.bind("dcterms", DCTERMS)

    def add_source_triples(temp_graph, source_file):
        """
        For each rdfs:Class in the temp_graph, add a dcterms:source triple with the filename.
        """
        for s in temp_graph.subjects(RDF.type, RDFS.Class):
            combined_graph.add((s, DCTERMS.source, Literal(source_file)))

    # Check if CIDOC CRM file exists
    if not os.path.isfile(cidoc_file):
        print(f"ERROR: Main CIDOC CRM file not found: {cidoc_file}")
        sys.exit(1)

    # Load the main CIDOC CRM ontology
    print(f"Loading CIDOC CRM ontology: {cidoc_file}")
    temp_graph = Graph()
    temp_graph.parse(cidoc_file, format=source_format)
    combined_graph += temp_graph
    add_source_triples(temp_graph, os.path.basename(cidoc_file))

    # Load each extension file
    for ext_file in extension_files:
        ext_path = os.path.join(extensions_dir, ext_file)
        if not os.path.isfile(ext_path):
            print(f"WARNING: Extension file not found, skipping: {ext_path}")
            continue
        print(f"Loading extension: {ext_path}")
        temp_graph = Graph()
        temp_graph.parse(ext_path, format=source_format)
        combined_graph += temp_graph
        add_source_triples(temp_graph, ext_file)

    print(f"Combined graph contains {len(combined_graph)} triples.")

    # Output file
    output_file = os.path.join(base_dir, "MaCHeCO.ttl")

    # Serialise combined graph as Turtle
    combined_graph.serialize(destination=output_file, format="turtle")
    print(f"Combined ontologies saved as: {output_file}")

if __name__ == "__main__":
    main()
