from settings import ENGINE_PATH
from sqlalchemy import create_engine
import pandas as pd
import datetime
from data.tldr.make_tldr_python import get_tldr_and_clean_text

KEYS_TO_REMOVE_FROM_REDDIT_RESULT = ["link_flair_richtext",
                                     "gildings",
                                     "preview"
                                     ]


class RedditToDb():

    def __init__(self,
                 save_to_table,
                 engine=ENGINE_PATH):
        self.engine = create_engine(engine)
        self.table_name = save_to_table
        self.cols = None

    def insert_submission_into_db(self, submission, if_exists="append"):
        df = self.subm_to_df(submission)
        df.to_sql(self.table_name, self.engine, if_exists=if_exists)

    def select_cols(self, sub_dict):
        if self.cols is None:
            sub_dict = {k: v for k, v in sub_dict.items()
                    if k not in KEYS_TO_REMOVE_FROM_REDDIT_RESULT}
            self.cols = sub_dict.keys()
        else:
            sub_dict = {k: v for k, v in sub_dict.items()
                    if k in self.cols}
        return sub_dict

    def subm_to_df(self, submission, add_tldr_cols=True):
        sub_dict = submission.d_
        sub_dict = self.select_cols(sub_dict)
        sub_dict["datetime_retrieved"] = datetime.datetime.now()
        if add_tldr_cols:
            sub_dict.update(get_tldr_and_clean_text(submission))
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
