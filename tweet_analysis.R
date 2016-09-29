setwd("~/Dropbox/Graduate School/Q4 - Autumn 2016/MSE231/Assignment1/MSE231-Assignment1")

library(scales)
library(dplyr)
library(ggplot2)
theme_set(theme_bw())

my_var <- "hello world"

# Load & format data
tweet_data <- read.csv("jm9_27tweets.csv", header=FALSE)
names(tweet_data) <- c("tweet_date","tweet_time","user_timezone")

# Count tweets by 15-minute interval
tweet_data_group_by <- group_by(tweet_data, tweet_date, tweet_time, user_timezone)
tweet_summary <- summarise(tweet_data_group_by, count = n())
tweet_summary$user_timezone <- factor(tweet_summary$user_timezone, levels=c("Eastern Time (US & Canada)", "Central Time (US & Canada)", "Mountain Time (US & Canada)", "Pacific Time (US & Canada)"), ordered=TRUE)

# Format dates
tweet_summary$date_time <- paste(tweet_summary$tweet_date, tweet_summary$tweet_time, sep = " ")
tweet_summary$date_time <- strptime(tweet_summary$date_time, format = "%Y-%m-%d %H:%M:%S")

## Remove edges
edge_times <- c(min(tweet_summary$date_time),max(tweet_summary$date_time))
tweet_summary <- tweet_summary[tweet_summary$date_time != edge_times[1] & tweet_summary$date_time != edge_times[2],]

# Plot tweets over time
tweet_plot <- ggplot(data=tweet_summary, aes(x=date_time, y=count, group=user_timezone, colour=user_timezone)) +
  geom_line() +
  geom_point() +
  scale_y_continuous(labels = scales::comma) +
  labs(title = "Number of Tweets (Per Quarter-Hour)", x = "", y = "") +
  scale_colour_discrete(name="Timezone",
                      breaks=c("Eastern Time (US & Canada)", "Central Time (US & Canada)", "Mountain Time (US & Canada)", "Pacific Time (US & Canada)"),
                      labels=c("EST", "CST", "MST", "PST"))
ggsave(plot=tweet_plot, file='Unfiltered_Tweets.pdf', width=6, height=4)
