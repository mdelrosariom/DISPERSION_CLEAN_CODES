library("readxl")
library("ggplot2")
#-------------------------------------------------------------------------------
# for 10 percent and 10 years
#-------------------------------------------------------------------------------
total_data <- data.frame()
info_all_simus_10_per_10_years <- data.frame()
for (i in 0:9){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/10_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists[info$number_of_generalists !=0], na.rm = T), "abundance_specialist" = mean((info$number_of_especialist[info$number_of_especialist!=0]), na.rm=T), 
                          "first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1],
                          "first_colonization_of_island" =which(info$island_populated != "0")[1], "percentage_occupation_generalists"= sum(info$number_of_generalists!=0)/1000, 
                          "percentage_occupation_especialists"= sum(info$number_of_especialist!="0")/1000)
  info_all_simus_10_per_10_years <- rbind(info_all_simus_10_per_10_years, info_simu)
}
#-------------------------------------------------------------------------------
# for 50 percent and 10 years
#-------------------------------------------------------------------------------
total_data <- data.frame()
info_all_simus_50_per_10_years <- data.frame()
for (i in 0:9){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/50_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists[info$number_of_generalists !=0], na.rm = T), "abundance_specialist" = mean((info$number_of_especialist[info$number_of_especialist!=0]), na.rm=T), 
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
for (i in 0:9){
  info <- read.csv(paste0("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL/100_per_10_annes_", i,".csv"))
  info$simulation <- i
  total_data <- rbind(total_data, info)
  info_simu <- data.frame("abundance_generalists"= mean(info$number_of_generalists[info$number_of_generalists !=0], na.rm = T), "abundance_specialist" = mean((info$number_of_especialist[info$number_of_especialist!=0]), na.rm=T), 
                          "first_colonization_generalists"= which(info$number_of_generalists != "0")[1], "first_colonization_especialists"= which(info$number_of_especialist!= "0")[1],
                          "first_colonization_of_island" =which(info$island_populated != "0")[1], "percentage_occupation_generalists"= sum(info$number_of_generalists!=0)/1000, 
                          "percentage_occupation_especialists"= sum(info$number_of_especialist!="0")/1000)
  info_all_simus_100_per_10_years <- rbind(info_all_simus_100_per_10_years, info_simu)
}

#===============================================================================
#==now we plot
#===============================================================================
pdf("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/DATA_FAST_ORIGINAL/abundance_plot_mean_abundance_W0_0.pdf",
    width = 3.35,   # ancho una columna
    height = 3.35,  # cuadrado prolijo
    family = "Helvetica")


abundance <- data.frame(group=as.character(), type= as.character(), value=as.numeric() )
abundance <- rbind(abundance, data.frame(treatment= "10%", type ="Generalists", value =info_all_simus_10_per_10_years$abundance_generalists ))
abundance <- rbind(abundance, data.frame(treatment= "10%", type ="Specialists", value =info_all_simus_10_per_10_years$abundance_specialist ))
abundance <- rbind(abundance, data.frame(treatment= "50%", type ="Generalists", value =info_all_simus_50_per_10_years$abundance_generalists ))
abundance <- rbind(abundance, data.frame(treatment= "50%", type ="Specialists", value =info_all_simus_50_per_10_years$abundance_specialist ))
abundance <- rbind(abundance, data.frame(treatment= "100%", type ="Generalists", value =info_all_simus_100_per_10_years$abundance_generalists ))
abundance <- rbind(abundance, data.frame(treatment= "100%", type ="Specialists", value =info_all_simus_100_per_10_years$abundance_specialist ))

abundance$treatment <- factor(abundance$treatment, c("10%", "50%", "100%"))
my_comparisons <-list(c("10%", "50%"), c("10%", "100%"), c("50%", "100%"))
ggplot(data = abundance, aes(x = treatment, y = value, fill = type)) +
  geom_boxplot() +
  scale_fill_manual(values = c("#FFFAFA" , "#CDC9C9"))+
  theme_bw()+
  stat_compare_means(method="anova")+
  stat_compare_means(comparisons = my_comparisons, method = "t.test")
