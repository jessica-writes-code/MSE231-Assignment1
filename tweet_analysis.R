setwd("~/Dropbox/Graduate School/Q4 - Autumn 2016/MSE231/Assignment1/MSE231-Assignment1")

library(dplyr)
library(ggplot2)
theme_set(theme_bw())

# Load & rename data
tweet_data <- read.csv("jm9_27tweets.csv", header=FALSE)
names(tweet_data) <- c("tweet_date","tweet_time","user_timezone")

# Count tweets by 15-minute interval
tweet_data_group_by <- group_by(tweet_data, tweet_time, user_timezone)
tweet_summary <- summarise(tweet_data_group_by, count = n())

# Plot tweets over time
ggplot(data=tweet_summary, aes(x=tweet_time, y=count, group=user_timezone, colour=user_timezone)) +
  geom_line() +
  geom_point()
