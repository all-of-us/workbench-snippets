# This plot assumes that most_recent_measurement_of_interest.sql has been run.
options(repr.plot.height = 20, repr.plot.width = 16)

most_recent_measurement_of_interest_df %>%
    filter(value_as_number < 9999999) %>% # Get rid of nonsensical outliers.
    mutate(age_at_measurement = year(as.period(interval(start = birth_datetime, end = measurement_date)))) %>%
    ggplot(aes(x = cut_width(age_at_measurement, width = 10, boundary = 0), y = value_as_number)) +
    geom_boxplot() +
    stat_summary(fun.data = get_boxplot_fun_data, geom = 'text', size = 4,
                 position = position_dodge(width = 0.9), vjust = -0.8) +
#    scale_y_log10() +  # Uncomment if the data looks skewed.
    coord_flip() +
    facet_wrap(~ sex_at_birth, nrow = length(unique(most_recent_measurement_of_interest_df$sex_at_birth))) +
    xlab('age') +
    ylab(str_glue('{UNIT_NAME}')) +
    labs(title = str_glue('Most recent {MEASUREMENT_NAME} measurement\nper person, by age, faceted by sex_at_birth'),
         caption = 'Source: All Of Us Data')
