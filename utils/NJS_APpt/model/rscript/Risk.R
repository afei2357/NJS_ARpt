 

##########preprocess################
#' Title
#'
#' @param data 
#' @param varnames 
#' @return dataframe
#' @export
#' @examples 
#' 

pkgs <- c("readxl","tidyverse","ropls","dplyr","optparse")
for(pkg in pkgs){suppressMessages(library(pkg,character.only = T))}

option_list <- list(
  make_option("--newdata",type="character",help="matrix to be predicted"),
  make_option("--model",type="character",help="PLS-DA model"),
  make_option("--variables",type="character",help="feature variables"),
  make_option("--rawdata",type="character",help="raw data of urine organic acids"),
  make_option("--outdir",type="character",help="outdir")
)
opt <- parse_args(OptionParser(option_list = option_list, 
                               usage="\nRscript %prog <newdata> <plsmodel.rds> <varnames.rds> <njs1_2.rds> <outdir>",
                               description = "\nCaculate risk of having urinary stones"))
newdata <- opt$newdata
model <- opt$model
varnames <- opt$variables
rawdata <- opt$rawdata
outdir <- opt$outdir
if(!dir.exists(outdir)){dir.create(outdir,recursive=TRUE)}



preprocess <- function(data,variables){
  data <- read_xlsx(data)
  data <- as.data.frame(data)
  variables <- readRDS(variables)
  variables <- c("实验号", "肌酐", variables)
  dat <- data %>% select(variables)
  dat$"性别" <- ifelse(dat$"性别"=="男",1,0)
  #dat$年龄 <- as.integer(format(Sys.Date(),"%Y"))-as.integer(format(dat$出生年月,"%Y"))
  #dat <- dat[,c(!(colnames(dat) %in% c("出生年月")))]
  dat <- dat %>% select("实验号", "肌酐", everything()) 
  return(dat)
}

risk_evaluation <- function(data, plsdamodel, variables, rawdata ,outdir){
  #data: "data frame",
  #plsdamodel:"logical" "TRUE"use the pls model builted by the training set
  #
  #Merge datasets
  dat <- preprocess(data,variables)
  #Creatinine correction
  for(i in 6:ncol(dat)){
    dat[, i] <- dat[,i]/dat[,"肌酐"]
  }
  #write.csv(dat,file =paste0(outdir, "/data1.norm.csv"),row.names=FALSE)

  #read model and variables
  plsModel <- readRDS(plsdamodel)
  varnames <- readRDS(variables)#variables contains age and gender

  njs1_2 <- readRDS(rawdata)
  vars <- varnames[-1]
  means <- data.frame(apply(njs1_2[,c(match(vars,colnames(njs1_2)))],2,mean))
  colnames(means) <- "mean"
  means <- data.frame(t(means))
  sds <- data.frame(apply(njs1_2[,c(match(vars,colnames(njs1_2)))],2,sd))
  colnames(sds) <- "sd"
  sds <- data.frame(t(sds))
  # scale
  scale_data <- dat[,-c(1:3)]
  for(i in 1:ncol(scale_data)){
      scale_data[, i] <- (scale_data[,i]-means[,i])/sds[,i]
    }
  whole_data <- cbind(dat[,c(1:3)],scale_data)
  
  #model predict 
  predict_pls <- predict(plsModel,newdata = whole_data[,c(match(varnames,colnames(whole_data)))])
  
  #split high medium and low risk
  highrisk <- 0.6865758
  lowrisk <- 0.2937039
  output <- cbind(select(whole_data,"实验号"), as.data.frame(predict_pls))
  for (i in 1:nrow(output)) {
    if(output$predict_pls[i] >= highrisk){
       output$risk[i] = "high"
     }else{
       if(output$predict_pls[i] < lowrisk){
         output$risk[i] = "low"
       }else{output$risk[i] = "medium"
       }
     }
    }
  write.csv(output,file =paste0(outdir, "/predict_risk.csv"),row.names=FALSE)
}


risk_evaluation(data = newdata, plsdamodel = model, variables = varnames, rawdata = rawdata,outdir = outdir)

#' 
#' 
#' 
