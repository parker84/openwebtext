import praw
import psaw
import tqdm
import datetime
from data.openwebtext.insert_reddit_submission_into_db import RedditToDb
from settings import REDDIT_POST_TABLE, URLS_SAVE_PATH


def scrape_reddit_api_and_save(query,
                               save_urls_path=URLS_SAVE_PATH,
                               save_to_table=REDDIT_POST_TABLE):
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
                url = subm.url
                # weird issue with psaw/pushshift that breaks score=">2"
                # if subm.score < 3:
                #     continue
                # print(subm.score)
    #            pbar.write(str(datetime.datetime.fromtimestamp(subm.created_utc)))
                reddit_to_db.insert_submission_into_db(subm)
                pbar.update(1)
                fh.write(url + '\n')
            fh.flush()

if __name__ == "__main__":

    api = psaw.PushshiftAPI()
    end_time = int(datetime.datetime(2019, 6, 1).timestamp())
    # start_time = int(datetime.datetime(2000, 6, 1).timestamp())

    query = api.search_submissions(
        before=end_time,
        # after=start_time,
        limit=100,
        sort='desc',
        score='>2',
        is_self=False,
        over_18=False)

    scrape_reddit_api_and_save(query)