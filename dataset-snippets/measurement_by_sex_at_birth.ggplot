# Use snippet 'measurement_by_sex_at_birth' to plot joined demographics and measurements dataframes.
# This plot assumes 'measurement_df' was created using snippet 'Basic operations -> join_dataframes' to
# join together demographics and measurements dataframes.
# See also https://r4ds.had.co.nz/data-visualisation.html


options(repr.plot.height = 10, repr.plot.width = 16)

# There could be many different measurements in the dataframe. By default, plot the first one.
measurement_to_plot <- unique(measurement_df$standard_concept_name)[1]

measurement_df %>%
    filter(standard_concept_name == measurement_to_plot) %>%
    filter(!unit_concept_name %in% c('No matching concept', 'NULL')) %>%
    filter(value_as_number < 9999999) %>%  # Get rid of nonsensical outliers.
    ggplot(aes(x = sex_at_birth, y = value_as_number)) +
    geom_boxplot() +
    stat_summary(fun.data = get_boxplot_fun_data, geom = 'text', size = 4,
                 position = position_dodge(width = 0.9), vjust = -0.8) +
#    scale_y_log10() +  # Uncomment if the data looks skewed.
    facet_wrap(standard_concept_name ~ unit_concept_name, ncol = 2, scales = 'free') +
    labs(title = str_glue('Numeric values of measurements, by sex_at_birth'), caption = 'Source: All Of Us Data') +
    theme(axis.text.x = element_text(angle=25, hjust=1))
