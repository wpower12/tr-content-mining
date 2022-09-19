"""
I'd like to track the 'migrations' and stuff I'd need in order to spin the entire database up on another machine.
So all the database creation, etc.

I'm sure this will use some stuff from the db module.
"""

SQL_USER_TABLES = [
    """ 
    CREATE TABLE `user_twitter` (
        `user_twitter_id` BIGINT(20) NOT NULL,
        `user_twitter_name` VARCHAR(32),
        PRIMARY KEY (`user_twitter_id`)
    ); 
    """,
    """ 
    CREATE TABLE `user_reddit` (
        `user_reddit_id` VARCHAR(16) NOT NULL,
        `user_reddit_name` VARCHAR(32),
        PRIMARY KEY (`user_reddit_id`)
    ); 
    """
]

SQL_CONTENT_TABLES = [
    """
    CREATE TABLE `content_tweet` (
        `tweet_id` BIGINT(20) NOT NULL,
        `user_twitter_id` BIGINT(20) NOT NULL,
        `text` TEXT(280),
        `datetime` DATETIME, 
        `retweets` INT DEFAULT 0, 
        PRIMARY KEY (`tweet_id`),
        FOREIGN KEY (`user_twitter_id`) REFERENCES `user_twitter`(`user_twitter_id`),
        FULLTEXT `ft_idx` (`text`)
    ) ENGINE=InnoDB;
    """,
    """
    CREATE TABLE `content_post` (
        `post_id` VARCHAR(16) NOT NULL,
        `user_reddit_id` VARCHAR(16) NOT NULL,
        `text` LONGTEXT,
        `datetime` DATETIME,
        `score` INT default 0,
        PRIMARY KEY (`post_id`),
        FOREIGN KEY (`user_reddit_id`) REFERENCES `user_reddit`(`user_reddit_id`),
        FULLTEXT `ft_idx` (`text`)
    ) ENGINE=InnoDB;
    """,
    """
    CREATE TABLE `content_comment` (
        `comment_id` VARCHAR(16) NOT NULL,
        `parent_id` VARCHAR(16) NOT NULL,
        `user_reddit_id` VARCHAR(16) NOT NULL,
        `text` LONGTEXT,
        `datetime` DATETIME,
        `score` INT default 0,
        PRIMARY KEY (`comment_id`),
        FOREIGN KEY (`user_reddit_id`) REFERENCES `user_reddit`(`user_reddit_id`),
        FULLTEXT `ft_idx` (`text`)
    ) ENGINE=InnoDB;
    """,

]

SQL_CONTEXT_TABLES = [
    """
    CREATE TABLE `context` (
        `context_id` INT NOT NULL AUTO_INCREMENT,
        `experiment_id` VARCHAR(32) NOT NULL,
        `context_desc` VARCHAR(64) NOT NULL,
        `context_query` LONGTEXT NOT NULL,
        PRIMARY KEY (`context_id`)
    ); 
    """,
    """
    CREATE TABLE `context_tweet` (
        `context_id` INT NOT NULL,
        `content_tweet_id` BIGINT(20) NOT NULL,
        FOREIGN KEY (`context_id`) REFERENCES `context`(`context_id`),
        FOREIGN KEY (`content_tweet_id`) REFERENCES `content_tweet`(`tweet_id`)
    );
    """,
    """
    CREATE TABLE `context_post` (
        `context_id` INT NOT NULL,
        `content_post_id` VARCHAR(16) NOT NULL,
        FOREIGN KEY (`context_id`) REFERENCES `context`(`context_id`),
        FOREIGN KEY (`content_post_id`) REFERENCES `content_post`(`post_id`)
    );
    """,
    """
    CREATE TABLE `context_comment` (
        `context_id` INT NOT NULL,
        `content_comment_id` VARCHAR(16) NOT NULL,
        FOREIGN KEY (`context_id`) REFERENCES `context`(`context_id`),
        FOREIGN KEY (`content_comment_id`) REFERENCES `content_comment`(`comment_id`)
    );
    """
]

SQL_SND_TABLES = [
    """
    CREATE TABLE `snd_subreddit` (
        `subreddit_id` VARCHAR(16) NOT NULL,
        `subreddit_name` VARCHAR(32),
        PRIMARY KEY (`subreddit_id`)
    );
    """,
    """ ALTER TABLE `content_post` ADD COLUMN `subreddit` VARCHAR(16); """,
    """ ALTER TABLE `content_comment` ADD COLUMN `subreddit` VARCHAR(16); """,
    """ ALTER TABLE `content_post` ADD FOREIGN KEY (`subreddit`) REFERENCES `snd_subreddit`(`subreddit_id`); """,
    """ ALTER TABLE `content_comment` ADD FOREIGN KEY (`subreddit`) REFERENCES `snd_subreddit`(`subreddit_id`); """,
    """
    CREATE TABLE `snd_hashtags` (
        `hashtag` VARCHAR(16) NOT NULL,
        `tweet_id` BIGINT(20) NOT NULL,
        FOREIGN KEY (`tweet_id`) REFERENCES `content_tweet`(`tweet_id`)
    );
    """,
    """
    CREATE TABLE `snd_url` (
        `url_id` INT NOT NULL AUTO_INCREMENT,
        `url` LONGTEXT NOT NULL,
        `url_hash` CHAR(32),
        PRIMARY KEY (`url_id`)
    );
    """,
    """
    CREATE TABLE `snd_urls_tweets` (
        `url_id` INT NOT NULL,
        `tweet_id` BIGINT(20) NOT NULL,
        FOREIGN KEY (`url_id`) REFERENCES `snd_url`(`url_id`),
        FOREIGN KEY (`tweet_id`) REFERENCES `content_tweet`(`tweet_id`)
    );
    """,
    """
    CREATE TABLE `snd_urls_posts` (
        `url_id` INT NOT NULL,
        `post_id` VARCHAR(16) NOT NULL,
        FOREIGN KEY (`url_id`) REFERENCES `snd_url`(`url_id`),
        FOREIGN KEY (`post_id`) REFERENCES `content_post`(`post_id`)
    );
    """,
    """
    CREATE TABLE `snd_urls_comments` (
        `url_id` INT NOT NULL,
        `comment_id` VARCHAR(16) NOT NULL,
        FOREIGN KEY (`url_id`) REFERENCES `snd_url`(`url_id`),
        FOREIGN KEY (`comment_id`) REFERENCES `content_comment`(`comment_id`)
    );
    """,
    """
    CREATE TABLE `snd_mentioned_users` (
        `tweet_id` BIGINT(20) NOT NULL,
        `user_twitter_id` BIGINT(20) NOT NULL,
        FOREIGN KEY (`tweet_id`) REFERENCES `content_tweet`(`tweet_id`),
        FOREIGN KEY (`user_twitter_id`) REFERENCES `user_twitter`(`user_twitter_id`)
    );
    """
]

def create_schema(cnx, db_name, drop_existing=False):
    cur = cnx.cursor()
    if drop_existing:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name};")

    cur.execute(f"CREATE DATABASE {db_name};")
    cur.execute(f"USE {db_name};")

    print("creating user tables.")
    for sql in SQL_USER_TABLES:
        cur.execute(sql)

    print("creating content tables")
    for sql in SQL_CONTENT_TABLES:
        cur.execute(sql)

    print("creating context tables")
    for sql in SQL_CONTEXT_TABLES:
        cur.execute(sql)

    print("creating snd tables")
    for sql in SQL_SND_TABLES:
        cur.execute(sql)

    




