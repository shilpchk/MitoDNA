library(gplots)

numberSamples=6
numberGroups=2
h1 <- read.table("20141102-005244S.tsv", header=F, sep="\t")
g1=c(1,1,1,2,2,2)
H1=t(h1[3:(2+numberSamples)])
ex1 = aov(H1~g1)

n=dim(h1)[[1]]
p=0
for(i in 1:n) {
   p[i]=summary(ex1)[[i]][[1,"Pr(>F)"]]
}

data1=h1[1,]

for(i in 2:n) {
   if(p[i]<0.05)
   data1=rbind(data1,h1[i,])
}

pdf("plot1.pdf")
heatmap.2(as.matrix(data1[3:(2+numberSamples)]), Colv=FALSE, trace='none', scale="row", col=greenred(60))
dev.off()


h2 <- read.table("20141102-005244Gr.tsv", header=F, sep="\t")
g2=c(1,2)
H2=t(h2[3:(2+numberGroups)])
ex2 = aov(H2~g2)

n=dim(h2)[[1]]
p=0
for(i in 1:n) {
   p[i]=summary(ex2)[[i]][[1,"Pr(>F)"]]
}

data2=h2[1,]

for(i in 2:n) {
   if(p[i]<0.05)
   data2=rbind(data2,h2[i,])
}

heatmap.2(as.matrix(data2[3:(2+numberGroups)]), Colv=FALSE, trace='none', scale="row", col=greenred(60))


