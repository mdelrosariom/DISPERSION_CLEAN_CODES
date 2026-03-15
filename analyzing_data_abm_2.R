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
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists, na.rm = T), "abundance_specialist" = mean((info$number_of_especialist), na.rm=T))
  info_all_simus_10_per_10_years <- rbind(info_all_simus_10_per_10_years, info_simu)
}
data_esp_10 <- data.frame("abundance"=info_all_simus_10_per_10_years$abundance_specialist, "type"="especialist")
data_gen_10 <- data.frame("abundance"=info_all_simus_10_per_10_years$abundance_generalists, "type"="generalist")

data_abu_10 <- rbind(data_esp_10, data_gen_10)

total_data <- data.frame()
info_all_simus_10_per_10_years_0 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists[info$number_of_generalists!=0], na.rm = T), "abundance_specialist" = mean((info$number_of_especialist[info$number_of_especialist!=0]), na.rm=T))
  info_all_simus_10_per_10_years_0 <- rbind(info_all_simus_10_per_10_years_0, info_simu)
  
}
data_esp_10_0 <- data.frame("abundance"=info_all_simus_10_per_10_years_0$abundance_specialist, "type"="especialist")
data_gen_10_0 <- data.frame("abundance"=info_all_simus_10_per_10_years_0$abundance_generalists, "type"="generalist")

data_abu_10_0 <- rbind(data_esp_10_0, data_gen_10_0)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(abundance ~group, data = data_abu_10)
data_abu_10 %>%
  group_by(type) %>%
  identify_outliers(abundance)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_abu_10 %>%
  group_by(type) %>%
  shapiro_test(abundance)

ggqqplot(data_abu_10, x = "abundance", facet.by = "type")

#Check the equality of variances
#This can be done using the Levene’s test. 
#If the variances of groups are equal, the p-value should be greater than 0.05.

data_abu_10 %>% levene_test(abundance ~ type)

#computation
stat.test <- data_abu_10 %>% 
  t_test(abundance ~ type) %>%
  add_significance()
stat.test

#data does not follow normal distribution so we apply a non parametric 
#test to compare the two groups 
wilcox.test(abundance ~ type, data = data_abu_10)

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
#PERMANENCE OF POPULATION
#===============================================================================

total_data <- data.frame()
perm_10 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("permanence_of_generalists"= sum(info$number_of_generalists!=0)/500, "permanence_of_especialists"= sum(info$number_of_especialist!="0")/500)
perm_10 <- rbind(perm_10, info_simu)
}
perm_gen_10 <- data.frame("permanence"=perm_10$permanence_of_generalists, "type"="generalist")
perm_esp_10 <- data.frame("permanence"=perm_10$permanence_of_especialists, "type"="especialist")

data_perm_10 <- rbind(perm_gen_10, perm_esp_10)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(permanence ~type, data = data_perm_10)
data_perm_10 %>%
  group_by(type) %>%
  identify_outliers(permanence)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_perm_10 %>%
  group_by(type) %>%
  shapiro_test(permanence) #not normal

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
wilcox.test(permanence ~ type, data = data_perm_10)

#===============================================================================
#=============================FOR 5O % 

total_data <- data.frame()
perm_50 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/50_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("permanence_of_generalists"= sum(info$number_of_generalists!=0)/500, "permanence_of_especialists"= sum(info$number_of_especialist!="0")/500)
  perm_50 <- rbind(perm_50, info_simu)
}
perm_gen_50 <- data.frame("permanence"=perm_50$permanence_of_generalists, "type"="generalist")
perm_esp_50 <- data.frame("permanence"=perm_50$permanence_of_especialists, "type"="especialist")

data_perm_50 <- rbind(perm_gen_50, perm_esp_50)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(permanence ~type, data = data_perm_50)
data_perm_10 %>%
  group_by(type) %>%
  identify_outliers(permanence)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_perm_50 %>%
  group_by(type) %>%
  shapiro_test(permanence) #not normal

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
wilcox.test(permanence ~ type, data = data_perm_50)
#===============================================================================
#=============================FOR 5O % 

total_data <- data.frame()
perm_100 <- data.frame()
for (i in 0:99){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/100_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("permanence_of_generalists"= sum(info$number_of_generalists!=0)/500, "permanence_of_especialists"= sum(info$number_of_especialist!="0")/500)
  perm_100 <- rbind(perm_100, info_simu)
}
perm_gen_100 <- data.frame("permanence"=perm_100$permanence_of_generalists, "type"="generalist")
perm_esp_100 <- data.frame("permanence"=perm_100$permanence_of_especialists, "type"="especialist")

data_perm_100 <- rbind(perm_gen_100, perm_esp_100)

#we need to know if it fullfills the assumtions for normality to apply tests

#1. Identify outliers by groups

boxplot(permanence ~type, data = data_perm_100)
data_perm_10 %>%
  group_by(type) %>%
  identify_outliers(permanence)

##2. Check normality by groups

# Compute Shapiro wilk test by goups

data_perm_100 %>%
  group_by(type) %>%
  shapiro_test(permanence) #not normal

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
wilcox.test(permanence ~ type, data = data_perm_100)

