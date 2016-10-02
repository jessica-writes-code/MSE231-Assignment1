setwd("~/Dropbox/Graduate School/Q4 - Autumn 2016/MSE231/Assignment1/MSE231-Assignment1")

library(scales)
library(dplyr)
library(ggplot2)
theme_set(theme_bw())

generate_graph <- function(in_filename, out_filename) {
  
  # Load & format data
  in_filename_txt = paste(in_filename, ".txt", sep="")
  tweet_data <- read.table(in_filename_txt, header=FALSE, sep="\t")
  names(tweet_data) <- c("tweet_date","tweet_time","user_timezone")

  # Count tweets by 15-minute interval
  tweet_data_group_by <- group_by(tweet_data, tweet_date, tweet_time, user_timezone)
  tweet_summary <- summarise(tweet_data_group_by, count = n())
  tweet_summary$user_timezone <- factor(tweet_summary$user_timezone, levels=c("Eastern Time (US & Canada)", "Central Time (US & Canada)", "Mountain Time (US & Canada)", "Pacific Time (US & Canada)"), ordered=TRUE)

  # Format dates
  tweet_summary$date_time <- paste(tweet_summary$tweet_date, tweet_summary$tweet_time, sep = " ")
  tweet_summary$date_time <- as.POSIXct(strptime(tweet_summary$date_time, format = "%Y-%m-%d %H:%M:%S"))

  ## Remove edges
  edge_times <- c(min(tweet_summary$date_time),max(tweet_summary$date_time))
  tweet_summary <- tweet_summary[tweet_summary$date_time != edge_times[1] & tweet_summary$date_time != edge_times[2],]

  # Plot tweets over time
  plot_title = paste("Number of", out_filename, "Tweets (Per Quarter-Hour)", sep=" ")
  tweet_plot <- ggplot(data=tweet_summary, aes(x=date_time, y=count, group=user_timezone, colour=user_timezone)) +
    geom_line() +
    geom_point() +
    scale_y_continuous(labels = scales::comma) +
    labs(title = plot_title, x = "", y = "") +
    scale_colour_discrete(name="Timezone",
                        breaks=c("Eastern Time (US & Canada)", "Central Time (US & Canada)", "Mountain Time (US & Canada)", "Pacific Time (US & Canada)"),
                        labels=c("EST", "CST", "MST", "PST"))
  
  # Save as vector formats
  out_filename_pdf = paste(out_filename, "_Tweets.pdf", sep="")
  ggsave(plot=tweet_plot, file=out_filename_pdf, width=6, height=4)
}

in_files = c("unfiltered_tweets", "filtered_tweets")
out_files = c("Unfiltered", "Filtered")

for (i in 1:2) {
  generate_graph(in_files[i], out_files[i])
}