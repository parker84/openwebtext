from settings import ENGINE_PATH, REDDIT_POST_TABLE
from sqlalchemy import create_engine
import pandas as pd
import datetime

class RedditToDb():

    def __init__(self,
                 engine=ENGINE_PATH):
        self.engine = create_engine(engine)

    def insert_submission_into_db(self, submission, if_exists="append"):
        df = self.subm_to_df(submission)
        df.to_sql(REDDIT_POST_TABLE, self.engine, if_exists=if_exists)

    def subm_to_df(self, submission):
        sub_dict = submission.d_
        sub_dict["datetime_retrieved"] = datetime.datetime.now()
        return pd.DataFrame(
            [sub_dict]
        )

    # def insert_info_table(self, submission):
    #     query = f"""
    #         --sql
    #         insert into {REDDIT_POST_INFO_TABLE}
    #             (
    #                 domain
    #                 ,is_sef
    #                 ,link_flair_text
    #                 ,num_comments
    #                 ,over_18
    #                 ,score
    #                 ,subreddit
    #                 ,subreddit_id
    #                 ,subreddit_subscribers
    #                 ,title
    #                 ,url
    #                 ,score
    #                 ,selftext
    #             )
    #     """