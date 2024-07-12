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

total_rows <- nrow(dat)

# Calculate the percentage of objects that meet >5.08cm criteria for each metric
percent_summary <- dat %>%
  pivot_longer(cols = object_size_type_diameter:object_size_type_major_axis,
               names_to = 'metric',
               values_to = 'value' ) %>%
  group_by(metric, value) %>%
  summarise(percent_greater = n() / total_rows) %>% 
  # Rename the values in metric
  mutate(metric = case_when(
    metric == 'object_size_type_area' ~ 'Area',
    metric == 'object_size_type_diameter' ~ 'Diameter',
    metric == 'object_size_type_major_axis' ~ 'Major Axis'
  ))

# Visualize that summary
ggplot() +
  geom_col(percent_summary, mapping = aes(x = metric, y = percent_greater, fill = value)) +
  coord_flip() +
  scale_fill_manual('olivedrab', 'ivory') +
  labs(
    title = 'Percent of segmented objects classified as greater or less than 5.08cm',
    fill = 'Object Classification',
    x = 'Metric by which object was classified',
    y = 'Percent of objects classified'
  ) +
  theme_classic()
