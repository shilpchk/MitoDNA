bwa index $1
for i in $(cat input.csv)
do
	if [ $(echo $i | awk -F, '{print $2}') -eq 1 ] ; then
		x=$(echo $i| awk -F, '{print $1}') 
		y=$(echo $i| awk -F, '{print $3}') 
		sai=$(echo $x | awk -F_ '{print $1}')	
		bwa aln $1 $x > $sai_1.sai 
		bwa aln $1 $y > $sai_2.sai 
		bwa sampe $1 $sai_1.sai $sai_2.sai $x $y > $sai.sam
	else
	 	x=$(echo $i| awk -F, '{print $1}')  
       		sai=$(echo $x | awk -F_ '{print $1}')
        	bwa aln $1 $x > $sai_1.sai             
     		bwa samse $1 $sai_1.sai $x > $sai.sam
	fi

	samtools view -bS $sai.sam > $sai.bam
	samtools sort $sai.bam $sai.sorted
	samtools rmdup $sai.sorted.bam $sai.sorted.ddup.bam
	samtools index $sai.sorted.ddup.bam
	samtools faidx sequence.fasta
	samtools mpileup -A -M 60 -f sequence.fasta $sai.sorted.ddup.bam > $sai.pileup
	perl pileup_parser.pl $sai.pileup 3 5 6 4 20 50 No Yes 2 $sai_filtered.pileup Yes No
done

