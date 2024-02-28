from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import config
import pandas as pd


###def function

def shortpara(coin_name, category_id):
    # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    # parameters = {
    #     'slug': coin_name,
    #     'convert': 'USD'
    # }
    # headers = {
    #     'Accepts': 'application/json',
    #     'X-CMC_PRO_API_KEY': config.coinmarketcap_keySecret,
    # }
    #
    # session = Session()
    # session.headers.update(headers)
    # index = 0

    Col = ['Coin Name', 'Current Price', 'Marketcap', 'FDV']

    try:
        #####single coin price
        # response = session.get(url, params=parameters)
        # data = json.loads(response.content)['data']
        # # print(json.dumps(data, indent=2))
        # for item in data: index = item
        # details = data[index]
        # tags = details['tags'] ##list
        # quotes = details['quote']
        # current_price = (quotes['USD']['price'])
        # market_cap = (quotes['USD']['market_cap'])
        # fully_diluted_market_cap = (quotes['USD']['fully_diluted_market_cap'])
        # print(f'coin: {coin_name}, '
        #       f'price: {current_price}, '
        #       f'marketcap: {market_cap}, '
        #       f'FDV: {fully_diluted_market_cap}, '
        #       f'tags: {tags}')

        ######category
        url_category = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories'
        parameters_category = {

            'slug': coin_name
        }
        headers_category = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.coinmarketcap_keySecret,
        }
        session_category = Session()
        session_category.headers.update(headers_category)
        response_category = session_category.get(url_category, params=parameters_category)


        data_category = json.loads(response_category.content)['data']

        for category_details in data_category:
            category_id = category_details['id']
            category_name = category_details['name']
            print(f'category: {category_name}, id: {category_id}')

        #######search by category id
        url_category_id = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
        parameters_category_id = {

            'id': category_id,
            'limit': 20
        }
        headers_category_id = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.coinmarketcap_keySecret,
        }
        session_category_id = Session()
        session_category_id.headers.update(headers_category_id)
        response_category_id = session_category_id.get(url_category_id, params=parameters_category_id)

        data_category_id = json.loads(response_category_id.content)
        coins_details = data_category_id['data']['coins']
        coin_index = 1
        coin_name_list_string = ""
        for coin_details in coins_details:
            found_coin_name = coin_details['slug']
            coin_name_list_string = coin_name_list_string + found_coin_name.lower() + ","

            print(f'coin{coin_index}: {found_coin_name}')
            coin_index += 1
        coin_name_list_string = coin_name_list_string[:-1]
        # print(coin_name_list_string)

        #######find list of coins details
        url_by_name_list = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters_by_name_list = {
            'slug': coin_name_list_string,
            'convert': 'USD'
        }
        headers_by_name_list = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.coinmarketcap_keySecret,
        }

        session_by_name_list = Session()
        session_by_name_list.headers.update(headers_by_name_list)
        response_by_name_list = session_by_name_list.get(url_by_name_list, params=parameters_by_name_list)


        data_by_name_list = json.loads(response_by_name_list.content)['data']
        aggregated_list = []
        for final_coin_details_index in data_by_name_list:
            sublist = []
            final_coin_details = data_by_name_list[final_coin_details_index]
            # print(final_coin_details)
            final_coin_name = final_coin_details['slug']
            final_coin_price = final_coin_details['quote']['USD']['price']
            final_coin_marketcap = final_coin_details['quote']['USD']['market_cap']
            final_coin_fdv = final_coin_details['quote']['USD']['fully_diluted_market_cap']

            sublist.append(final_coin_name)
            sublist.append(final_coin_price)
            sublist.append(final_coin_marketcap)
            sublist.append(final_coin_fdv)
            aggregated_list.append(sublist)

            # print(f'coin: {final_coin_name}, price: {final_coin_price}, marketcap: {final_coin_marketcap}, FDV: {final_coin_fdv}')

        ##generate df and csv
        new_df = pd.DataFrame(columns=Col, data=aggregated_list).sort_values(by=['FDV'], ascending=False)
        print(new_df)
        file_name = f'{coin_name}.csv'
        new_df.to_csv(f'results/{file_name}', index=False)
        print(f'{file_name} is generated\n')


    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


##todo run the function
coin_data_frame = pd.read_csv('coin and category map.csv', header=0)

for row in range(len(coin_data_frame)):

    coin_name = coin_data_frame.iloc[row]['coin']
    category_id = str(coin_data_frame.iloc[row]['categoryID'])
    print(f'coin: {coin_name}, category: {coin_data_frame.iloc[row]['category']}, categoryID: {category_id}')
    shortpara(coin_name, category_id)
