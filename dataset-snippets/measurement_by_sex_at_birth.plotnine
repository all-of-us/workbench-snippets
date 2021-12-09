# Use snippet 'measurement_by_sex_at_birth' to plot joined demographics and measurements dataframes.
# This plot assumes 'measurement_df' was created using snippet 'Basic operations -> join_dataframes' to
# join together demographics and measurements dataframes.
# See also https://plotnine.readthedocs.io/en/stable/


# There could be many different measurements in the dataframe. By default, plot the first one.
measurement_to_plot = measurement_df.standard_concept_name.unique()[0]

# meas_filter is a column of True and False.
meas_filter = ((measurement_df.standard_concept_name == measurement_to_plot)
  & (measurement_df.unit_concept_name != 'No matching concept')
  & (measurement_df.unit_concept_name.notna())
  & (measurement_df.value_as_number < 9999999)  # Get rid of nonsensical outliers.
)

(ggplot(measurement_df[meas_filter], aes(x = 'sex_at_birth', y = 'value_as_number')) +
    geom_boxplot() +
    stat_summary(fun_data = get_boxplot_fun_data, geom = 'text', size = 10,
                 position = position_dodge(width = 0.9), va = 'top') +
#    scale_y_log10() +  # Uncomment if the data looks skewed.
    facet_wrap(('standard_concept_name', 'unit_concept_name'), ncol = 2, scales = 'free') +
    ggtitle(f'Numeric values of measurements, by sex_at_birth\nSource: All Of Us Data') +
    theme(figure_size=(12, 6), panel_spacing = .5, axis_text_x = element_text(angle=25, hjust=1)))
