# This plot assumes that measurement_of_interest.sql has been run.

# meas_filter is a column of True and False
meas_filter = measurement_of_interest_df['value_as_number'] < 9999999 # Get rid of nonsensical outliers.
(ggplot(measurement_of_interest_df[meas_filter], aes(x = 'sex_at_birth', y = 'value_as_number')) +
    geom_boxplot() +
    stat_summary(fun_data = get_boxplot_fun_data, geom = 'text', size = 10,
                 position = position_dodge(width = 0.9), va = 'top') +
#    scale_y_log10() +  # Uncomment if the data looks skewed.
    ylab(f'{UNIT_NAME}') +
    ggtitle(f'All {MEASUREMENT_NAME} measurements, by site\nSource: All Of Us Data') +
    theme(figure_size=(12, 6), axis_text_x = element_text(angle=25, hjust=1)))
