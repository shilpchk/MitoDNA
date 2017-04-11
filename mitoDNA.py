import csv
import commands
import os
import sys
import time
from hetero import *
cmd = " "

global space
global row
global arg
cr = csv.reader(open("input.csv","rb"))
row = cr.next()
arg = row[0]
cmd = "bwa index " + arg
space = " "
os.system(cmd)

row = cr.next()
numberSamples=int(row[0])
row = cr.next()
numberGroups=int(row[0])
row = cr.next()
qualityScore=int(row[0])
row = cr.next()
minreads=int(row[0])
row = cr.next()
threshold=float(row[0])


fileList = []
groups =[]
for row in cr:
     groups.append(int(row[3]))
     if row[1] == "1" :
        one=str(row[0]).split("_")
        sai1 = one[0]+"_1.sai"
        two=str(row[2]).split("_")
        sai2 = two[0]+"_2.sai"

        cmd1="bwa aln "+ arg +space+ row[0]+ space +" >  "+ sai1
        print cmd1
        cmd2="bwa aln "+ arg +space+ row[2]+ space +" >  "+ sai2
        print cmd2
        os.system(cmd1)
        os.system(cmd2)
        sam=one[0]+".sam"
        cmd3 = "bwa sampe "+arg +space + sai1+space + sai2+space + row[0]+space+row[2] + " > " + sam
     else:
        one=str(row[0])
        sai = one[0].sai
        cmd1="bwa aln "+ arg +space+ row[0]+space +" >  "+ sai
        os.system(cmd1)
        sam=one[0]+".sam"
        cmd3 = "bwa samse "+arg +space + sai+space + row[0]+space + " > " + sam
     os.system(cmd3)

     bam=one[0]+".bam"
     cmd4 = "samtools view -bS " +sam + space + ">  "+bam
     os.system(cmd4)

     srtd=one[0]+".sorted"
     cmd5= "samtools sort  " +bam + space + srtd
     os.system(cmd5)

     sortedbam = srtd+".bam"
     sortedddupbam = srtd+".ddup.bam"
     cmd6 = "samtools rmdup " + sortedbam +space + sortedddupbam
     os.system(cmd6)

     cmd7 = "samtools index " + sortedddupbam
     os.system(cmd7)

     cmd8 = "samtools faidx " + arg
     os.system(cmd8)

     pileup=one[0]+".pileup"
     cmd9 = "samtools mpileup -A -M 60 -f " + arg +space +sortedddupbam +" > " +pileup
     os.system(cmd9)

     fpileup=one[0]+"F.pileup"
     cmd10 = "perl pileup_parser.pl" + space+ pileup+space+" 3 5 6 4 " + str(qualityScore)+ space + str(minreads)+ " No Yes 2"+space + fpileup + " Yes No"
     os.system(cmd10)

     filteredTSV=one[0]+".tsv"
     filterMinReads(fpileup, filteredTSV, minreads)
 
     polyfullTSV = one[0]+"Pfull.tsv"
     polyTSV     = one[0]+"P.tsv"
     fileList.append(polyTSV)
     idenPolymorphism(filteredTSV, polyfullTSV, polyTSV, threshold)

timestr = time.strftime("%Y%m%d-%H%M%S")
outfile1=timestr+"S.tsv"
joinPropDatasets(fileList, outfile1)

outfile2=timestr+"Gr.tsv"
with open(outfile1, 'rb') as tsvin, open(outfile2, 'wb') as tsvout:
     tsvin  = csv.reader(tsvin, delimiter='\t')
     tsvout = csv.writer(tsvout, delimiter='\t')
     for r in tsvin:
        newr=[]
        value=[]
        for i in range(numberGroups):
           value.append(0)
        for i in range(numberSamples):
           value[groups[i]-1] += float(r[2+i])
        newr.append(r[0])
        newr.append(r[1])
        for i in range(numberGroups):
           newr.append(value[i])
        tsvout.writerow(newr)

