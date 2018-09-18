import requests
import copy
from bs4 import BeautifulSoup
from django.conf import settings
from django.forms.models import model_to_dict

from gpscraper.models import AppData, AppSearchIndex
from gpscraper.decorators import return_none_if_error

PLAY_STORE_URL = getattr(
    settings, 'PLAY_STORE_URL', "https://play.google.com/store"
)

SEARCH_RESULT_COUNT = getattr(settings, 'SEARCH_RESULT_COUNT', 1)


class PlayStoreHelper(object):

    def __get_data_from_db(term):
        """
        Return the data from database, if information for `term` exists.
        otherwise returns `None`
        """
        try:
            index = AppSearchIndex.objects.get(query=term)
        except AppSearchIndex.DoesNotExist:
            index = None
        if index:
            apps_data = index.apps.all().values()
            return apps_data
        return None

    def __set_data_to_db(term, data):
        """
        Create database index of `term` for `data`.
        """
        data_copy = copy.deepcopy(data)
        instances = []
        for app_data in data_copy:
            instance, created = AppData.objects.get_or_create(
                uid=app_data.pop('uid'), **app_data)
            instances.append(instance)
        index, created = AppSearchIndex.objects.get_or_create(query=term)
        index.apps.add(*instances)

    def __get_data_from_store(term):
        """
        Get the data from PlayStore for the `term` by parsing.
        """
        url_search = PLAY_STORE_URL + "/search"
        response = requests.get(url_search, {'c': 'apps', 'q': term})
        soup = BeautifulSoup(response.content, "html.parser")
        apps = soup.find_all("div", {"class": "card no-rationale square-cover apps small"})

        result = []
        print(result)
        for i, app in enumerate(apps):
            app_details_basic = app.find("div", {"class": "details"})
            app_id = app['data-docid']
            app_data = {
                'uid': app_id,
                'name': app_details_basic.find("a", {"class": "title"})['title'].strip().encode('utf-8'),
                'dev_name': app_details_basic.find("a", {"class": "subtitle"})['title'].strip(),
                'icon_url': "http://" + app.find(
                    "div", {"class": "cover-inner-align"}).img['data-cover-large'].strip("//")
            }

            url_app_detail = PLAY_STORE_URL + "/apps/details"
            response = requests.get(url_app_detail, {'id': app_id})
            soup = BeautifulSoup(response.content, "html.parser")

            app_data.update({
                'category': soup.find("a", {"itemprop": "genre"}).text,
                'description': soup.find("div", {"itemprop": "description"}).text.strip().encode('utf-8'),
                
            })

           
            dev_links = soup.find_all("a", {"class": "dev-link", "rel": "nofollow"})
            if dev_links:
                for dev_link in dev_links:
                    if "mailto" in dev_link['href']:
                        app_data['dev_email'] = dev_link['href'].replace("mailto:", "")
                        break

            result.append(app_data)

            if i + 1 == SEARCH_RESULT_COUNT:
                break
            print(result)
        return result

    @classmethod
    # @return_none_if_error
    def search(self, term):
        """
        Performs the search for the `term` and returns `data` from
        database if exists, otherwise by parsing from playstore.
        """
        data = self.__get_data_from_db(term)

        if not data:
            data = self.__get_data_from_store(term)
            self.__set_data_to_db(term, data)
            print(data)
        return data
        

    @classmethod
    @return_none_if_error
    def get_app_details(self, app_id):
        """
        Returns the details of app from database given the `app_id`.
        """
        app_data = AppData.objects.get(uid=app_id)
        return model_to_dict(app_data)