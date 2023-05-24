# In the field of fiscal and political studies, there exist data that needs to be aggregated on a fiscal year basis. 
# In this case, we cannot simply subset the units for analysis based solely on the numeric value of the year. 
# Therefore, this code provides a method for aggregating event data on a fiscal year basis. 
# This analysis assumes the setting of analyzing units such as political years and fiscal years based on political conventions as potential applications.

# Install necessary packages
install.packages(c("tidyverse", "readr", "lubridate", "ggplot2", "gridExtra", "pdfTools"))

# Load the packages
library(tidyverse)
library(readr)
library(lubridate)
library(ggplot2)
library(gridExtra)
library(openxlsx)

# Read all csv files in a directory into a list
files <- list.files(path="data", pattern="*.csv", full.names=TRUE)
# The data structure is as follows:
# Year Month Content Note
# 2015	1	Verification	None
# 2015	1	Verification	None
# 2015	1	Analysis	None
# 2015	1	Contact	None
# 2015	1	Verification	None

# Read all csv files and combine them into a single dataframe
all_data <- files %>% map_df(~read_csv(., locale = locale(encoding = "Shift-JIS")))

# Export the combined dataframe as a csv
write_csv(all_data, "binded.csv")

binded <- read.table("binded.csv", sep = ",", header = T)

# Generate the fiscal year
colnames(binded) <- c("year", "month", "content", "note")
binded$FY <- ifelse(binded$month < 4, binded$year - 1, binded$year)

# Count the data for each fiscal year, specify the target fiscal year in subset: this time it's 2013-2022
yearly_counts <- binded %>% count(FY) %>% subset(., subset = (FY <= 2022 & FY >= 2013))
yearly_counts

write.xlsx(yearly_counts, "count.xlsx")

# Plot the data on a bar graph
p1 <- ggplot(yearly_counts, aes(x=FY, y=n)) +
  geom_col(fill="steelblue") +
  labs(x="Fiscal Year", y="Count", subtitle = "subtitle") +
  ggtitle("Counts per Fiscal Year") +
  theme_minimal() + 
  scale_x_continuous(breaks = seq(min(yearly_counts$FY), max(yearly_counts$FY), by = 1)) 
print(p1)

ggsave("figures/count.jpg", plot = p1)
ggsave("figures/count.pdf", plot = p1, device = cairo_pdf)

# Count data by fiscal year and category
yearly_category_counts <- binded %>% count(FY, content)

# Create pie charts
colnames(binded) <- c("year", "month", "category", "note", "FY")

pie_plots <- binded %>%
  count(FY, category) %>%
  group_by(FY) %>%
  mutate(Percentage = n / sum(n)) %>%
  ungroup() %>%
  split(.$FY)

pie_plots <- binded %>%
  count(FY, category) %>%
  group_by(FY) %>%
  mutate(Percentage = n / sum(n)) %>%
  ungroup() %>%
  split(.$FY) %>%
  map(~ ggplot(., aes(x = "", y = Percentage, fill = category)) +
        geom_bar(width = 1, stat = "identity") +
        coord_polar("y", start = 0) +
        theme_void() + 
        labs(title = paste0(unique(.$FY), " Breakdown of Contents", fill = "")))
