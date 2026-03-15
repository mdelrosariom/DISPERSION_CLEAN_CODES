library(tidyverse)
library(rstatix)
library(ggpubr)
#-------------------------------------------------------------------------------
# for 10 percent and 10 years
#-------------------------------------------------------------------------------
total_data <- data.frame()
info_all_simus_10_per_10_years <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists, na.rm = T), "abundance_specialist" = mean((info$number_of_especialist), na.rm=T), 
                          "first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1],
                          "first_colonization_of_island" =which(info$island_populated != "0")[1], "percentage_occupation_generalists"= sum(info$number_of_generalists!=0)/1000, 
                          "percentage_occupation_especialists"= sum(info$number_of_especialist!="0")/1000)
  info_all_simus_10_per_10_years <- rbind(info_all_simus_10_per_10_years, info_simu)
}
data_esp_10 <- data.frame("abundance"=info_all_simus_10_per_10_years$abundance_specialist, "type"="especialist")
data_gen_10 <- data.frame("abundance"=info_all_simus_10_per_10_years$abundance_generalists, "type"="generalist")

data_abu_10 <- rbind(data_esp_10, data_gen_10)
#===============================================================================
# 10% without zeros in generalist check 
#===============================================================================
total_data_0 <- data.frame()
info_all_simus_10_per_10_years_0 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data_0 <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean((info$number_of_generalists[info$number_of_generalists!=0]), na.rm = T), 
                          "abundance_specialist" = mean((info$number_of_especialist[info$number_of_especialist!=0]), na.rm=T))
  info_all_simus_10_per_10_years_0 <- rbind(info_all_simus_10_per_10_years_0, info_simu)
}
data_esp_10_0 <- data.frame("abundance"=info_all_simus_10_per_10_years$abundance_specialist, "type"="especialist")
data_gen_10_0 <- data.frame("abundance"=info_all_simus_10_per_10_years$abundance_generalists, "type"="generalist")

data_10_0 <- rbind(data_esp_10_0, data_gen_10_0)
#-------------------------------------------------------------------------------
# for 50 percent and 10 years
#-------------------------------------------------------------------------------
total_data <- data.frame()
info_all_simus_50_per_10_years <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/50_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists, na.rm = T), "abundance_specialist" = mean((info$number_of_especialist), na.rm=T), 
                          "first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1],
                          "first_colonization_of_island" =which(info$island_populated != "0")[1], "percentage_occupation_generalists"= sum(info$number_of_generalists!=0)/1000, 
                          "percentage_occupation_especialists"= sum(info$number_of_especialist!="0")/1000)
  info_all_simus_50_per_10_years <- rbind(info_all_simus_50_per_10_years, info_simu)
}


#-------------------------------------------------------------------------------
# for 100 percent and 10 years
#-------------------------------------------------------------------------------
total_data <- data.frame()
info_all_simus_100_per_10_years <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/100_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists, na.rm = T), "abundance_specialist" = mean((info$number_of_especialist), na.rm=T), 
                          "first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1],
                          "first_colonization_of_island" =which(info$island_populated != "0")[1], "percentage_occupation_generalists"= sum(info$number_of_generalists!=0)/1000, 
                          "percentage_occupation_especialists"= sum(info$number_of_especialist!="0")/1000)
  info_all_simus_100_per_10_years <- rbind(info_all_simus_100_per_10_years, info_simu)
}

#===============================================================================
#info_all_simus_10_per_10_years
#===============================================================================
#WE FIRST NEED TO ANALYZE THE DIFFERENCE BETWEEN GENERALISTS AND ESPECIALISTS IN EACH ENVIRONMENT
#for this we can use an independent t test that compares two groups where you compare means of two independent
#groups.

#Assumtions: 
#Independence of the observations. Each subject should belong to only one group. There is no relationship between the observations in each group.
#yes
#No significant outliers in the two groups

#Normality. the data for each group should be approximately normally distributed.
#Homogeneity of variances. the variance of the outcome variable should be equal in each group.

#1. Identify outliers by groups

data_species_10 <- rbind(data_esp_10, data_gen_10)

data_species_10 %>%
  group_by(type) %>%
  identify_outliers(abundance)

##2. Check normality by groups

# Compute Shapiro wilk test by goups


data(data_species_10, package = "datarium")
data_species_10 %>%
  group_by(type) %>%
  shapiro_test(abundance)

ggqqplot(data_species_10, x = "abundance", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_species_10 %>% levene_test(abundance ~ type)

#computation
stat.test <- data_species_10 %>% 
  t_test(abundance ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(abundance ~ type, data = data_species_10)


#do the same for 50% 

#===============================================================================
#info_all_simus_10_per_10_years
#===============================================================================
#make a df with data on abundances
data_gen_50 <- data.frame("abundance"= info_all_simus_50_per_10_years$abundance_generalists, type="generalists")
data_gen_50 <- data.frame("abundance"= info_all_simus_50_per_10_years$abundance_specialist, type="especialists")

#1. Identify outliers by groups

data_species_50 <- rbind(data_esp_50, data_gen_50)

data_species_50 %>%
  group_by(type) %>%
  identify_outliers(abundance)

##2. Check normality by groups

# Compute Shapiro wilk test by goups


data(data_species_50, package = "datarium")
data_species_50 %>%
  group_by(type) %>%
  shapiro_test(abundance)

ggqqplot(data_species_50, x = "abundance", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_species_50 %>% levene_test(abundance ~ type)

#computation
stat.test <- data_species_10 %>% 
  t_test(abundance ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
boxplot(abundance~type, data= data_species_50)
wilcox.test(abundance ~ type, data = data_species_50)

#===============================================================================
#info_all_simus_100_per_10_years
#===============================================================================
#make a df with data on abundances
data_gen_100 <- data.frame("abundance"= info_all_simus_100_per_10_years$abundance_generalists, type="generalists")
data_gen_100 <- data.frame("abundance"= info_all_simus_100_per_10_years$abundance_specialist, type="especialists")

#1. Identify outliers by groups

data_species_100 <- rbind(data_esp_100, data_gen_100)
boxplot(abundance~type, data= data_species_100)
data_species_100 %>%
  group_by(type) %>%
  identify_outliers(abundance)

##2. Check normality by groups

# Compute Shapiro wilk test by goups


data(data_species_100, package = "datarium")
data_species_100 %>%
  group_by(type) %>%
  shapiro_test(abundance)

ggqqplot(data_species_100, x = "abundance", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_species_100 %>% levene_test(abundance ~ type)

#computation
stat.test <- data_species_100 %>% 
  t_test(abundance ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
boxplot(abundance~type, data= data_species_100)
wilcox.test(abundance ~ type, data = data_species_100)


#===============================================================================
# 10% without zero in abundance
#===============================================================================

data_10_0 %>%
  group_by(type) %>%
  identify_outliers(abundance)

##2. Check normality by groups

# Compute Shapiro wilk test by goups


data(data_10_0, package = "datarium")
data_10_0 %>%
  group_by(type) %>%
  shapiro_test(abundance) #not normal!

ggqqplot(data_species_10, x = "abundance", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_species_10 %>% levene_test(abundance ~ type)

#computation
stat.test <- data_species_10 %>% 
  t_test(abundance ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(abundance ~ type, data = data_10_0)


#===============================================================================
#===============================================================================
#=======================NOW WE ANALYZE FIRST COLONIZATION 
#===============================================================================
total_data <- data.frame()
first_col_10 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1])
  first_col_10 <- rbind(first_col_10, info_simu)
}
fc_gen_10 <- data.frame("first_colonization"=first_col_10$first_colonization_generalists, "type"="generalist")
fc_esp_10 <- data.frame("first_colonization"=first_col_10$first_colonization_especialists, "type"="especialist")

data_fc_10 <- rbind(fc_gen_10, fc_esp_10)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(first_colonization ~type, data = data_fc_10)
data_fc_10 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_10 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(first_colonization ~ type, data = data_fc_10)

#===============================================================================
#=============================FOR 5O % 

total_data <- data.frame()
first_col_50 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/50_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1])
  first_col_50 <- rbind(first_col_50, info_simu)
}
fc_gen_50 <- data.frame("first_colonization"=first_col_50$first_colonization_generalists, "type"="generalist")
fc_esp_50 <- data.frame("first_colonization"=first_col_50$first_colonization_especialists, "type"="especialist")

data_fc_50 <- rbind(fc_gen_50, fc_esp_50)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(first_colonization ~type, data = data_fc_50)
data_fc_50 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_50 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(first_colonization ~ type, data = data_fc_50)

#===============================================================================
#=============================FOR 100 % 

total_data <- data.frame()
first_col_100 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/100_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1])
  first_col_100 <- rbind(first_col_100, info_simu)
}
fc_gen_100 <- data.frame("first_colonization"=first_col_100$first_colonization_generalists, "type"="generalist")
fc_esp_100 <- data.frame("first_colonization"=first_col_100$first_colonization_especialists, "type"="especialist")

data_fc_100 <- rbind(fc_gen_100, fc_esp_100)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(first_colonization ~type, data = data_fc_100)
data_fc_100 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_100 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(first_colonization ~ type, data = data_fc_100)

#===============================================================================
#===============================================================================
#=======================NOW WE ANALYZE MEAN AGE
#===============================================================================
mean_age_10 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info_simu <- data.frame("mean_age_generalists"= mean(info$mean_age_generalists), "mean_age_especialists"= mean(info$mean_age_especialists))
  print(info_simu)
  mean_age_10 <- rbind(mean_age_10, info_simu)
}
mean_age_gen_10 <- data.frame("mean_age"=mean_age_10$mean_age_generalists, "type"="generalist")
mean_age_esp_10 <- data.frame("mean_age"=mean_age_10$mean_age_especialists, "type"="especialist")

data_age_10 <- rbind(mean_age_gen_10, mean_age_esp_10)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(mean_age ~type, data = data_age_10)
data_fc_10 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_10 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(mean_age ~ type, data = data_age_10)

#===============================================================================
#=============================FOR 5O % 

mean_age_50 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/50_per_10_annes_", i,".csv"))
  info_simu <- data.frame("mean_age_generalists"= mean(info$mean_age_generalists), "mean_age_especialists"= mean(info$mean_age_especialists))
  mean_age_50 <- rbind(mean_age_50, info_simu)
}
mean_age_gen_50 <- data.frame("mean_age"=mean_age_50$mean_age_generalists, "type"="generalist")
mean_age_esp_50 <- data.frame("mean_age"=mean_age_50$mean_age_especialists, "type"="especialist")

data_age_50 <- rbind(mean_age_gen_50, mean_age_esp_50)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(mean_age ~type, data = data_age_50)
data_fc_10 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_10 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(mean_age ~ type, data = data_age_50)
#===============================================================================
#=============================FOR 100 % 
mean_age_100 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/100_per_10_annes_", i,".csv"))
  info_simu <- data.frame("mean_age_generalists"= mean(info$mean_age_generalists), "mean_age_especialists"= mean(info$mean_age_especialists))
  mean_age_100 <- rbind(mean_age_100, info_simu)
}
mean_age_gen_100 <- data.frame("mean_age"=mean_age_100$mean_age_generalists, "type"="generalist")
mean_age_esp_100 <- data.frame("mean_age"=mean_age_100$mean_age_especialists, "type"="especialist")

data_age_100 <- rbind(mean_age_gen_100, mean_age_esp_100)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(mean_age ~type, data = data_age_100)
data_fc_10 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_10 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(mean_age ~ type, data = data_age_100)



#===============================================================================
#===============================================================================
#=======================NOW WE DO PRESENCE TIME
#===============================================================================
pres_10 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info_simu <- data.frame("presence_generalists"= sum(info$number_of_generalists==0)/500, "presence_especialist"= sum(info$number_of_especialist==0)/500)
  pres_10 <- rbind(pres_10, info_simu)
}
p_gen_10 <- data.frame("presence"=pres_10$presence_generalists, "type"="generalist")
p_esp_10 <- data.frame("presence"=pres_10$presence_especialist, "type"="especialist")

pres10 <- rbind(p_gen_10, p_esp_10)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(presence ~type, data = pres10)
data_fc_10 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_10 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(presence ~ type, data = pres10)

#===============================================================================
#=============================FOR 5O % 

pres_50 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/50_per_10_annes_", i,".csv"))
  info_simu <- data.frame("presence_generalists"= sum(info$number_of_generalists==0)/500, "presence_especialist"= sum(info$number_of_especialist==0)/500)
  pres_50 <- rbind(pres_50, info_simu)
}
p_gen_50 <- data.frame("presence"=pres_50$presence_generalists, "type"="generalist")
p_esp_50 <- data.frame("presence"=pres_50$presence_especialist, "type"="especialist")

pres50 <- rbind(p_gen_50, p_esp_50)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(presence ~type, data = pres50)
data_fc_50 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_50 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(presence ~ type, data = pres50)

#===============================================================================
#=============================FOR 100 % 
pres_100 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/100_per_10_annes_", i,".csv"))
  info_simu <- data.frame("presence_generalists"= sum(info$number_of_generalists==0)/500, "presence_especialist"= sum(info$number_of_especialist==0)/500)
  pres_100 <- rbind(pres_100, info_simu)
}
p_gen_100 <- data.frame("presence"=pres_100$presence_generalists, "type"="generalist")
p_esp_100 <- data.frame("presence"=pres_100$presence_especialist, "type"="especialist")

pres100 <- rbind(p_gen_100, p_esp_100)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(presence ~type, data = pres100)
data_fc_50 %>%
  group_by(type) %>%
  identify_outliers(first_colonization)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_fc_50 %>%
  group_by(type) %>%
  shapiro_test(first_colonization) #not normal

ggqqplot(data_fc_10, x = "first_colonization", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_fc_10 %>% levene_test(first_colonization ~ type)

#computation
stat.test <- data_fc_10 %>% 
  t_test(first_colonization ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(presence ~ type, data = pres100)

pre_10_gen = data.frame("presence"=p_gen_10$presence, type ="10")
pre_50_gen = data.frame("presence"=p_gen_50$presence, type ="50")
pre_100_gen = data.frame("presence"=p_gen_100$presence, type ="100")

gen_pre = rbind(pre_10_gen, pre_50_gen, pre_100_gen)