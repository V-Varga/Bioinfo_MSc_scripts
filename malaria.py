#! /user/bin/python
"""
Title: malaria.py
Date: 2020-10-09
Author: Virág Varga

Description:
	This program uses the malaria.fna FASTA file and the malaria.blastx.tab file containing
		gene prodoct functions in order add those functions into the header lines
		of the FASTA sequences.
	The program exludes sequences with no assigned functions from the final output.
	The script as written is limited to use with input files malaria.fna and malaria.blastx.tab;
		and an output file output.txt.

List of functions:
	No user-defined functions are used in the process.

List of "non standard" modules:
	No non-standard modules were used.

Procedure:
	1. A dictionary consisting of the sequence identifiers and the associated functions
		is built from the malaria.blastx.tab file.
	2. A dictionary consisting of the sequence headers and the associated gene sequences
		is built from the malaria.fna file.
	3. An output file is constructed wherein the identified functions of the gene products
		are added to the sequence headers from the FASTA file. Genes with functions
		listed as 'null' in the malaria.blastx.tab file are exluded from this output.

Usage:
	./malaria.py malaria.fna malaria.blastx.tab output.txt
	OR
	python malaria.py malaria.fna malaria.blastx.tab output.txt

This script was written for Python 3.8.5, in Spyder 4.
"""

#Step 1: creating a dictionary with sequence identifyers and protein functions

name_dict = {}
#creates an empty dictionary for the protein names

with open('malaria.blastx.tab') as infile:
	#opens the malaria.blastx.tab file for manipulation
	for line in infile:
		#the process below will be repeated line by line for the length of the malaria.blastx.tab file
		seq_name = line.strip().split()[0]
		#line.strip() removes the "\n" character as the end of the line
		#split here selects the column containing the sequence identifyers
		prot_funct = line.strip().split()[9]
		#split here selects the column containing the protein functions
		name_dict[seq_name] = prot_funct
		#the dictionary is filled using members of seq_name as the key and prot_funct as the associated value

name_dict
#print the dictionary to the console for cursory visual confirmation that the process worked


#Step 2: creating a dictionary from the malaria.fna file

fasta_dict = {}
#creates an empty dictionary that the fasta file will be turned into

with open('malaria.fna') as infile:
	#opens malaria.fna for manipulation
	for line in infile:
		if line.startswith('>'):
			#identifies the header lines by the fact that they start with the > character
			seq_header = line.strip().replace('>','')
			#creates a variable seq_header which contains the entire header line from malaria.fna, without the > and '\n' characters
		else:
			#for all non-header lines
			prot_seq = line.strip()
			#creates a variable that is just the sequence, without the '\n' character
			fasta_dict[seq_header] = prot_seq
			#fills the fasta_dict dictionary using seq_header as the key and prot_seq as the value

fasta_dict
#print the dictionary to the console for cursory visual confirmation that the process worked


#Step 3: joining the 2 dictionaries into the desired output.txt file

output = open('output.txt', 'w')
#create a new file to write to, called output.txt

for seq_header in fasta_dict:
	#now begin process of matching up the 2 dictionaries, using the fasta_dict as the main dictionary,
	#and identifying the seq_header key as what we will be working with
	seq_name2 = seq_header.split()[0]
	#create a new variable that contains just the sequence identifier portion of the sequence header
	if name_dict[seq_name2] != 'null':
		#uses the newly created variable seq_name2 as the key in the name_dict dictionary
		#checks to see whether the called value is 'null', and excludes such results from further commands
		output.write('>' + seq_header + '\t' + name_dict[seq_name2] + '\n')
		#writes the sequence header with the > character at the start, the original header, and the protein function at the end
		#also includes a '\n' character so that the next command will write into a new line
		output.write(fasta_dict[seq_header] + '\n')
		#writes out the sequence associated with the sequence header called and written in the command above
		#also includes a '\n' character so that the next command will write into a new line
