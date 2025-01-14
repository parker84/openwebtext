from settings import ENGINE_PATH
from sqlalchemy import create_engine
import pandas as pd
import datetime
from data.tldr.make_tldr_python import get_tldr_and_clean_text

KEYS_TO_REMOVE_FROM_REDDIT_RESULT = ["link_flair_richtext",
                                     "gildings",
                                     "preview",
                                     "author_flair_richtext",
                                     "all_awardings",
                                     "resized_icons"
                                     ]


class RedditToDb():

    def __init__(self,
                 save_to_table,
                 engine=ENGINE_PATH,
                 start_row=0):
        self.engine = create_engine(engine)
        self.table_name = save_to_table
        self.cols = None
        self.get_cols_currently_in_table()
        self.row_num = start_row

    def insert_submission_into_db(self, submission, if_exists="append"):
        df = self.subm_to_df(submission)
        df.to_sql(self.table_name, self.engine, if_exists=if_exists)

    def subm_to_df(self, submission, add_tldr_cols=True):
        sub_dict = submission.d_
        sub_dict = self.select_cols(sub_dict)
        sub_dict["datetime_retrieved"] = datetime.datetime.now()
        sub_dict["ix"] = self.row_num
        if add_tldr_cols:
            sub_dict.update(get_tldr_and_clean_text(submission))
            if sub_dict["tldr_summary"] is not None:
                sub_dict["len_tldr_summary"] = len(
                    sub_dict["tldr_summary"].split(" "))
            else:
                sub_dict["len_tldr_summary"] = 0
            if sub_dict["tldr_content"] is not None:
                sub_dict["len_tldr_content"] = len(
                    sub_dict["tldr_content"].split(" "))
            else:
                sub_dict["len_tldr_content"] = 0
        self.row_num += 1
        return pd.DataFrame(
            [sub_dict]
        )

    def get_cols_currently_in_table(self):
        try:
            df = pd.read_sql_query("select * from " + self.table_name + " limit 10",
                                   self.engine)
            self.curr_cols = list(df.columns)
        except Exception as error:
            print(error)
            self.curr_cols = None

    def select_cols(self, sub_dict):
        if self.cols is None:
            sub_dict = {k: v for k, v in sub_dict.items()
                        if k not in KEYS_TO_REMOVE_FROM_REDDIT_RESULT}
            self.cols = sub_dict.keys()
            if self.curr_cols is not None:
                self.cols = [col for col in self.cols
                             if col in self.curr_cols]
        sub_dict = {k: v for k, v in sub_dict.items()
                    if k in self.cols}
        return sub_dict

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
