library(tidyverse)
library(ggbeeswarm)

# Read in data
dat <- read_csv('image_measurements.csv') %>% 
  # Rename first column to be the ID
  rename(shape_id = ...1) %>% 
  # Get columns for whether area is "> 5.08cm" by several different metrics
  mutate(
    object_size_type_diameter = ifelse(equivalent_diameter > 5.08, '>5.08cm', '<=5.08cm'),
    object_size_type_area = ifelse(Area > 20.268299, '>5.08cm', '<=5.08cm'),
    object_size_type_major_axis = ifelse(MajorAxisLength > 5.08, '>5.08cm', '<=5.08cm')
    )

# Visualize data
ggplot() +
  geom_beeswarm(dat, mapping = aes(x = as.character(1), y = MajorAxisLength, color = object_size_type_major_axis))

# Calculate the percentage of objects that meet >5.08cm criteria for each metric
percent_summary <- dat %>% 
  pivot_longer(cols = object_size_type_diameter:object_size_type_major_axis, 
               names_to = 'metric', 
               values_to = 'value' ) %>% 
  group_by(metric) %>% 
  summarise(percent_greater = aslkdjflsdfkjl / n())
  # mutate(object_size_type_diameter = subset('>5.08cm') / n())
