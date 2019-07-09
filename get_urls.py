import praw
import psaw
import tqdm
import datetime
from data.openwebtext.insert_reddit_submission_into_db import RedditToDb
from settings import REDDIT_SELF_POST_TABLE, REDDIT_NON_SELF_POST_TABLE, \
    URLS_SAVE_PATH, REDDIT_COMMENTS_TABLE


def scrape_reddit_api_and_save(query,
                               save_urls_path=URLS_SAVE_PATH,
                               save_to_table=REDDIT_NON_SELF_POST_TABLE):
    """loop over the results from the api query, save them to the a db
    and save the urls to a txt
    
    Arguments:
        query {instace of api.search_submissions} -- where: api = psaw.PushshiftAPI()
        save_urls_path {str} -- path to save urls
    """
    reddit_to_db = RedditToDb(save_to_table)
    with tqdm.tqdm() as pbar:
        with open(save_urls_path, 'w') as fh:
            for subm in query:
                # import ipdb; ipdb.set_trace()
                # weird issue with psaw/pushshift that breaks score=">2"
                # if subm.score < 3:
                #     continue
                # print(subm.score)
    #            pbar.write(str(datetime.datetime.fromtimestamp(subm.created_utc)))
                reddit_to_db.insert_submission_into_db(subm)
                pbar.update(1)
                if "url" in subm.d_:
                    url = subm.url
                    fh.write(url + '\n')
            fh.flush()

if __name__ == "__main__":

    api = psaw.PushshiftAPI()
    end_time = int(datetime.datetime(2019, 6, 1).timestamp())
    # start_time = int(datetime.datetime(2000, 6, 1).timestamp())
    # search = "tl & dr"
    # search = "selftext:(tl & dr)"
    # search = "selftext:tl & dr"
    # search = "selftext:tl" 0
    # self_text_search = "tl & dr" bunch of meanigless results
    # self_text_search = "' tl' & 'dr'" 3 results
    

    #-------------self text search
    # TLDRs in self text (=> usually summarizing the reddit data)
    # self_text_search = "'tl' & 'dr'"
    # query = api.search_submissions(
    #     # q=search,
    #     selftext=self_text_search,
    #     before=end_time,
    #     # after=start_time,
    #     # limit=100,
    #     limit=100,
    #     sort='desc',
    #     score='>2',
    #     # is_self=False, 3 results when true w self_text_search = "'tl' & 'dr'"
    #     # 100 when either
    #     over_18=False)
    # 100 results






    #--------------url posts
    # TLDRS in title (=> usually summarizing the link)
    # search = "'tl' & 'dr'"
    # query = api.search_submissions(
    #     q=search,
    #     before=end_time,
    #     # limit=100,
    #     sort='desc',
    #     score='>2',
    #     is_self=False,
    #     over_18=False)
    # print(len(list(query)))
    # 8362
    # search = "'TL' & 'DR'"
    # query = api.search_submissions(
    #     q=search,
    #     before=end_time,
    #     # limit=100,
    #     sort='desc',
    #     score='>2',
    #     is_self=False,
    #     over_18=False)
    # print(len(list(query))) # 8362
    # search = "tl;dr"
    # query = api.search_submissions(
    #     q=search,
    #     before=end_time,
    #     # limit=100,
    #     sort='desc',
    #     score='>2',
    #     is_self=False,
    #     over_18=False)
    # print(len(list(query))) # 8362
    # search = "tldr"
    # query = api.search_submissions(
    #     q=search,
    #     before=end_time,
    #     # limit=100,
    #     sort='desc',
    #     score='>2',
    #     is_self=False,
    #     over_18=False)
    # print(len(list(query))) # 2190
    search = "'tl' & 'dr'"
    # query = api.search_submissions(
    #     q=search,
    #     before=end_time,
    #     # limit=100,
    #     sort='desc',
    #     score='=2',
    #     is_self=False,
    #     over_18=False)
    # print(len(list(query))) # 15975
    # query = api.search_submissions(
    #     q=search,
    #     before=end_time,
    #     # limit=100,
    #     sort='desc',
    #     score='=2',
    #     is_self=False)
    # print(len(list(quer           gfffgfgfgfgfgff                                                                                                                                                           nnnnnnnnnnnnnnnnnnnnnnnn                                                                                                                              ))) # 16439 not worth it
    query = api.search_submissions(
        q=search,
        before=end_time,
        # limit=100,
        sort='desc',
        score='>1',
        is_self=False,
        over_18=False)
    print(len(list(query))) # 9257
    scrape_reddit_api_and_save(query, REDDIT_NON_SELF_POST_TABLE)
    query = api.search_submissions(
        q=search,
        before=end_time,
        # limit=100,
        sort='desc',
        score='=2',
        is_self=False,
        over_18=False)
    scrape_reddit_api_and_save(query, REDDIT_NON_SELF_POST_TABLE)
    query = api.search_submissions(
        q=search,
        before=end_time,
        # limit=100,
        sort='desc',
        score='>2',
        is_self=False,
        over_18=False)
    scrape_reddit_api_and_save(query, REDDIT_NON_SELF_POST_TABLE)


    #-------------self posts all search
    # TLDRs in self text (=> usually summarizing the reddit data)
    search = "'tl' & 'dr'"
    query = api.search_submissions(
        q=search,
        before=end_time,
        # after=start_time,
        # limit=100,
        sort='desc',
        score='>2',
        is_self=True,
        # 100 when either
        over_18=False)
    scrape_reddit_api_and_save(query, save_to_table=REDDIT_SELF_POST_TABLE)
    query = api.search_submissions(
        q=search,
        before=end_time,
        # after=start_time,
        # limit=100,
        sort='desc',
        score='=2',
        is_self=True) # 
    scrape_reddit_api_and_save(query, save_to_table=REDDIT_SELF_POST_TABLE)


    # #--------------comments
    # # TODO: get comments working, last error was AttributeError: 'comment' object has no attribute 'url'
    # search = "test"
    # query = api.search_comments(
    #     q=search) # many results
    # query = api.search_comments(
    #     q=search,
    #     sort='desc',
    #     before=end_time,
    #     score='>2', # 0 results on or off
    #     # is_self=True, # 0 results on or off
    #     over_18=False) # 0 results
    # query = api.search_comments(
    #     q=search,
    #     before=end_time,
    #     score='>2', # 0 results on or off
    #     # is_self=True, # 0 results on or off
    #     over_18=False) # 0 results
    # query = api.search_comments(
    #     q=search,
    #     before=end_time,
    #     score='>2') # many results
    search = "'tl' & 'dr'"
    query = api.search_comments(
        q=search,
        sort='desc',
        before=end_time,
        score='>2')
    # print(len(list(query)))
    scrape_reddit_api_and_save(query, REDDIT_COMMENTS_TABLE)
    