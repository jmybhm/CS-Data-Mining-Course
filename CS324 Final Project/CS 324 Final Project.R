library(stringr)
library(car)

data <- read.delim("~/Documents/CS324/robust_length_activity.bed", stringsAsFactors = F)
colnames(data) <- c("Chr","Start","End","Length","Activity")
#changing "chrX" and "chrY" to "chr23" and chr24"
data[,1] <- str_replace(data[,1], "[X]", "23")
data[,1] <- str_replace(data[,1], "[Y]", "24")
#changing the first column into a numeric vector
data[,1] <- substr(data[,1],4,5)
data[,1] <- as.numeric(data[,1],4,5)

set.seed(7)
#k means clustering
k <- 7
km.out=kmeans(data[,c(1,4,5)],k,iter.max=1000, nstart=5, algorithm="Lloyd")
km.out
table(km.out$cluster)

#centroids for each cluster
km.out$center

#lattice plot
library(car)
scatterplotMatrix(data[,c(1,4,5)], groups=km.out$cluster, reg.line=F, smoother=F, legend.coords = "bottomright")


#plotting SS against cluster numbers
SSE <- lapply(2:15,function(x) kmeans(data[,c(1,4,5)],x,iter.max=1000, nstart=5, algorithm="Lloyd")$tot.withinss)
plot(2:15,unlist(SSE), xlab = "k", ylab="SSE", main="k vs. Total Clustering Error (SSE)")

#Association Rules
library(arules)
lung_binary <- read.csv("~/Downloads/lung_binary.csv")
lung_binary$Small_Cell_Lung_Carcinoma <- factor(lung_binary$Small_Cell_Lung_Carcinoma)
lung_binary$Squamous_Cell_Lung_Carcinoma <- factor(lung_binary$Squamous_Cell_Lung_Carcinoma)
lung_binary$Large_Cell_Lung_Carcinoma <- factor(lung_binary$Large_Cell_Lung_Carcinoma)
lung_binary$Lung_Adenocarcinoma <- factor(lung_binary$Lung_Adenocarcinoma)
lung_binary$Lung.adult <- factor(lung_binary$Lung.adult)
lung_binary$Lung.fetal <- factor(lung_binary$Lung.fetal)
lung_binary$Lung_Right_Lower_Lobe <- factor(lung_binary$Lung_Right_Lower_Lobe)

rules <- apriori(lung_binary,
                 parameter = list(minlen=2, supp=0.005, conf=0.8),
                 appearance = list(both=c("Small_Cell_Lung_Carcinoma=1", "Squamous_Cell_Lung_Carcinoma=1",
                              "Large_Cell_Lung_Carcinoma=1","Lung_Adenocarcinoma=1", "Lung.adult=1",
                              "Lung.fetal=1"),
                              default="none"),
                 control = list(verbose=F))
rules.sorted <- sort(rules, by="lift")
inspect(rules.sorted)



