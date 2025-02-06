# Integrating Facial Phenotype-Genotype-Disease Associations: A Knowledge Graph Platform for Personalized Analysis and Mechanistic Insights

---

## Overview
This repository contains resources, data supporting the publication **"Integrating Facial Phenotype-Genotype-Disease Associations in Human Genetics: A Knowledge Graph Platform for Personalized Analysis and Mechanistic Insights"**. The work introduces a comprehensive knowledge graph (FPGDKG) that integrates **genotype**, **facial phenotype**, and **disease** associations. 

---

## Repository Contents
This repository includes the following files and resources:
1. **`README.md`**  
    - This file provides detailed documentation for the repository, including file descriptions, and usage instructions.
2. **`Knowledge Graph file.dump`**  
    - This file contains a serialized dump of the knowledge graph (FPGDKG), representing the associations between facial phenotypes, genotypes, and diseases.  
    - You can load this file into a Neo4j database or any compatible graph database platform to replicate the analyses described in the publication.  

3. **`Search Terms.csv`**  
    - A CSV file containing  search terms described in the paper.
---

## How to Use

### 1. Loading the Knowledge Graph
- The `Knowledge Graph file.dump` can be loaded into a Neo4j database using the following steps:
  1. Install Neo4j on your system.
  2. Create a new database or use an existing database.
  3. Use the Neo4j Browser or Admin CLI to import the knowledge graph dump file:
     ```bash
     neo4j-admin load --from=<path_to_file.dump> --database=<database_name> --force
     ```
  4. Start the database and explore the graph using Cypher queries.

### 2. Querying the Graph
- Use the Cypher to queries the KG. 
