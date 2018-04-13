#!/usr/bin/env python
import sys
import os
from Bio import SeqIO
# vcf file input
filename = sys.argv[1]

# reference file input:
reffile = sys.argv[2]
handle = SeqIO.parse(open(reffile,"r"),"fasta")
for record in handle:
	print("name of reference:")
	print(record.id)
	refseq = record.seq
	reflen = len(refseq)
# I will just pad the beginning of the sequence and the end of the sequence if not  covered enough

# to store new consensus
conseq=""
# seqname
tmp  = os.path.basename(filename)
seqname = ">"+tmp.split(".")[0]


# file name output is just 
tmp = sys.argv[1].split("/")[-1]
outname = tmp+".fasta"

def parseinfo(info):
	resdic={}
	field = info.split(";")
	for item in field:
		c = item.split("=")
		vals=c[1].split(',')
		resdic[c[0]]=vals
	return resdic

with open(sys.argv[1],'r') as fin:
#	to store coverage
	dps=[]
	# To fill sequences for positions not covered by alignement (poor sequencing)
	posref=1 # start with one, take care of -1 when accessing position in sequence.
		
	for line in fin:
		if line[0]=="#":
			continue
		splited_line = line.split()
		pos = int(splited_line[1])
		print(pos)
		print(posref)
		if pos>posref:
			#			conseq += refseq[posref] # Maybe output two sequences: One with the ref bases in lower case, and the others with N
			conseq += "N"*(pos-posref+1)
			posref=pos+1
			continue
		if posref>pos:
			print("posref sup to pos!!!")
		refbase = splited_line[3]
		altbases = splited_line[4]
		altbases = altbases.split(",")	
		print(pos,refbase,altbases)
		infos = parseinfo(splited_line[7])
		dp = int(infos["DP"][0])
		dps.append(dp)
		if infos["NUMALT"][0]!="0":
			print(pos,refbase,altbases)
			refcount = int(infos["RO"][0])
			altcount = list(map(int,infos["AO"]))
			print(refcount,altcount,dp)	
			if refcount>=max(altcount):
				conseq+=refbase
				posref+=len(refbase)
			else:
				print("ALTERNATE BASE !")
				print(altcount)
				pos = altcount.index(max(altcount))
				print(altbases)
				conseq += altbases[pos]
				print(altbases[pos])
				print("DONE")
			# Advance from a size equal to seq
				posref+=len(altbases[pos])

		else:
			conseq+=refbase
			posref+=len(refbase)
conseq+="N"*(len(refseq)-len(conseq))

print("Length of resulting consensus:")
print(len(conseq))

seqname+="|"+str(sum(dps)/float(len(dps)))
fout = open(outname,'w')
fout.write(seqname+"\n")
for i in range(0,len(conseq),80):
	fout.write(conseq[i:i+80]+"\n")
fout.close()


