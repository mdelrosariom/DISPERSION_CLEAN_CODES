library(readxl)
library(openxlsx)
library(stringr) #to exclude patterns, we are going to try

#===============================================================================
#----------------------- CHUNK FOR COMPILE ALL OF THE SIMULATIONS---------------
# make 100 files, each one with the 1000 time steps as rows 

library(readxl)
library(openxlsx)
library(data.table)

for (i in 1:99) {   # 100 files (one per i)
  temp_list <- vector("list", 1000)  # 1000 rows (time steps)
  
  for (j in 1:999) {
    file_path <- paste0(
      "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/3_output_data_phase_1_1000_run_2_sps/sim_RAMI_50_",
      i, "_", j, ".xlsx"
    )
    temp_list[[j]] <-  read.xlsx(file_path) #faster than read_excel
  }
  print(i)
  compiled <- rbindlist(temp_list, fill = TRUE)
  
  write.xlsx(
    compiled,
    paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/RAMI_100_", i, ".xlsx")
  )
}
#===============================================================================
#==== I CHANGED TO CSV, MUCH FASTER SUPOSSELY 
#===============================================================================

library(data.table)

for (i in 1:99) {
  # list all csv files for this i
  files <- sprintf(
    "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/LAST_ORIGINAL/sim_RAMI_100_%d_%d.csv",
    i, 1:999
  )
  
  # read all at once
  temp_list <- lapply(files, fread)
  # bind in C (fast)
  compiled <- rbindlist(temp_list, fill = TRUE)
  fwrite(compiled,sprintf("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/LAST_ORIGINAL/RAMI_100_%d.csv",
      i))
  print(i)
}








#-------------- we should have 100 files per type of simulation (10,50,100)

files <- list.files(path = "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/", pattern = "RAMI_10", all.files = FALSE,
                    full.names = FALSE, recursive = FALSE,
                    ignore.case = FALSE, include.dirs = FALSE, no.. = FALSE)

for (i in 0:99){
  print(file.exists(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/compiled_rami_10_", i, ".xlsx")))
}

#we have all of the files, but the 100 is comp_sq_100_", i, ".xlsx" and the others 50_, i, ".xlsx or 10_

#===============================================================================
# I did the means, but it does not make so much sense because there are a lot of zeros 

compile <- function(type){
  
  means <- matrix(NA, nrow = 99, ncol = 3)
  colnames(means) <- c("sim","mean_generalists", "mean_especialists")
  
  for (i in 1:99) {
    file_path <- paste0(
      "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/RAMI_", 
      type, "_", i, ".xlsx"
    )
    
    info <- read_excel(file_path)
    means[i,1] <- i
    means[i, 2] <- mean(info$number_of_generalists, na.rm = TRUE)
    means[i, 3] <- mean(info$number_of_especialist, na.rm = TRUE)
  }
  
  output_path <- paste0(
    "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/summary_statistics/RAMI_",
    type,"_MEANS.xlsx"
  )
  
  write.xlsx(as.data.frame(means), output_path)
  
  return(as.data.frame(means))
}



#===============================================================================

means_100 <- read_excel("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/summary_statistics/RAMI_100_MEANS.xlsx")
means_50 <- read_excel("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/summary_statistics/RAMI_50_MEANS.xlsx")

#means_50 <- read_excel("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_ph_1/1A_50_MEANS_all.xlsx")

# Extract numeric vectors instead of tibbles
C <- list(
  as.numeric(means_10[[2]]),
  as.numeric(means_10[[3]])
)
C <- lapply(C, function(x) x[x != 0])
# Name the list
names(C) <- c(
  paste("generalist 50%"),
  paste("especialist 50%")
)

# Adjust mgp to avoid text overlap
par(mgp = c(3, 2, 0))

# Final boxplot
boxplot(C, col = "#69b3a2", ylab = "value")

t.test(means_10[[2]], means_10[[3]])


#===============================================================================
#for when you dont have exactly the number of simulations 

files <- list.files(path = "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/3_output_data_phase_1_1000_run_2_sps/", pattern = "comp_sq_100_", all.files = FALSE,
           full.names = TRUE)


# Preallocate: 99 rows, 2 columns
means_100 <- matrix(NA, nrow = length(files), ncol = 3)
colnames(means_100) <- c("sim","mean_generalists", "mean_especialists")

for (i in 1:length(files)) {
  file_path <- paste0(
    
   files[i]
  )
  
  info <- read_excel(file_path)
  means_100[i,1] <- i
  means_100[i, 2] <- mean(info$number_of_generalists, na.rm = TRUE)
  means_100[i, 3] <- mean(info$number_of_especialist, na.rm = TRUE)
}


write.xlsx(
  as.data.frame(means_30),
  "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_ph_1/1B_COMP_SQ_30_MEANS_all.xlsx"
)


#===============================================================================

means_30 <- read_excel("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_ph_1/1A_100_MEANS_all_SQ.xlsx")
#means_50 <- read_excel("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_ph_1/1A_50_MEANS_all.xlsx")

# Extract numeric vectors instead of tibbles
C <- list(
  as.numeric(means_30[[2]]),
  as.numeric(means_30[[3]])
)
C <- lapply(C, function(x) x[x != 0])
# Name the list
names(C) <- c(
  paste("generalist 100"),
  paste("especialist 100")
)

# Adjust mgp to avoid text overlap
par(mgp = c(3, 2, 0))

# Final boxplot
boxplot(C, col = "#69b3a2", ylab = "value")

t.test(means_30[[2]], means_30[[3]])

#===============================================================================


#===============================================================================
#--------------------------percentage of occupation-----------------------------
# i think i will do this because it makes more sense than using the mean. using the mean is not 
#good because you average runs in which species colonize the island with runs in which this does not 
#happen


occupation_100 <- matrix(NA, nrow = 99, ncol = 2)
colnames(occupation_100) <- c("freq_generalists", "freq_especialists")

for (i in 1:99) {
  file_path <- paste0(
    "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/RAMI_100_",
    i, ".xlsx"
  )
  
  info <- read_excel(file_path)
  
  generalists_count <- sum(info$number_of_generalists != 0)
  especialists_count <- sum(info$number_of_especialist != 0)
  
 
  occupation_100[i, 1] <- generalists_count / length(info$number_of_generalists)
  occupation_100[i, 2] <- especialists_count / length(info$number_of_especialist)
}

write.xlsx(
  as.data.frame(occupation_100),
  "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/OCCUPATION_all_sims_100.xlsx"
)

#===============================================================================
#===============================================================================


info <- read_excel("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/compiled_rami_version/OCCUPATION_all_sims_100.xlsx")

C <- list(
  as.numeric(info[[1]]),
  as.numeric(info[[2]])
)
##C <- lapply(C, function(x) x[x != 0])
# Name the list
names(C) <- c(
  paste("generalist 100"),
  paste("especialist 100")
)

# Final boxplot
boxplot(C, col = "#69b3a2", ylab = "value")

t.test(info[[1]], info[[2]])



#maybe corrected 24/10/25

