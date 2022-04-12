from re import L
from pprint import pprint
from typing import Dict, List, Tuple, Union
import psycopg2

# connecting to db named phone_recommender

connection = psycopg2.connect(user="postgres", password="60Db!e$$", host="127.0.0.1",
                              port="5432", database="phone_recommender")
cursor = connection.cursor()


def get_query_filters(filters) -> List[str]:
    # where_queries = ["WHERE socpoints = 12 OR displaypoints = 6 OR ram_storagepoints = 11 OR batterypoints = 9 OR speakerpoints = 6;"]
    condition_list = []
    if filters:
        # TODO: Implement This
        pass
    return condition_list


def get_max_values(filter_conditions: List[str]) -> Dict[str, int]:
    # where_condition = ''

    # data = {''}
    try:
        where_condition = ''
        if filter_conditions:
            where_condition = f"WHERE {' AND '.join(f'({_})' for _ in filter_conditions)}"
        postgreSQL_select_Query = f"""SELECT MAX(socpoints) AS biggest_soc_point,
            MAX(ram_storagepoints) AS biggest_ram_storage_point,
            MAX(displaypoints) AS biggest_display_point,
            MAX(batterypoints) AS biggest_battery_point,
            MAX(speakerpoints) AS biggest_speaker_point
        FROM mob_scores {where_condition};"""
        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        return {
            'socpoints': mobile_records[0][0],
            'ram_storagepoints': mobile_records[0][1],
            'displaypoints': mobile_records[0][2],
            'batterypoints': mobile_records[0][3],
            'speakerpoints': mobile_records[0][4],
        }

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def get_all_data_with_preferences(preferences, filters=None):
    if filters is None:
        filters = {}
    filter_conditions = get_query_filters(filters)
    max_value_dict = get_max_values(filter_conditions)
    phone_ids, pref_data = get_data_and_phone_ids_according_to_pref(max_value_dict, filter_conditions, preferences)
    print(phone_ids)
    db_data = get_sorted_data_without_preferences(phone_ids, filter_conditions)
    total_data = insert_to_sorted_array(db_data, pref_data)
    return total_data, phone_ids


def insert_to_sorted_array(sorted_data: List[Dict[str, Union[int, str]]],
                           data_to_insert: List[Dict[str, Union[int, str]]]) -> List[Dict[str, Union[int, str]]]:
    # TODO:Implement This
    sorted_data.extend(data_to_insert)
    sorted_data = sorted(sorted_data, key=lambda x: x['totalpoints'], reverse=True)
    return sorted_data


def get_sorted_data_without_preferences(phone_ids: List[str], filter_conditions: List[str]) -> List[
    Dict[str, Union[int, str]]]:
    # TODO:Implement This
    where_condition = ''
    total_data = []
    if filter_conditions:
        where_condition = f"AND {' AND '.join(f'({_})' for _ in filter_conditions)}"
    try:
        query_get_data = f"""SELECT *
                                        FROM mob_scores
                                        WHERE (phoneid NOT IN {str(tuple(phone_ids))}) {where_condition}
                                        ORDER BY totalpoints desc;"""
        cursor.execute(query_get_data)
        mobile_records = cursor.fetchall()
        for mobile_record in mobile_records:
            temp_json = {
                'socpoints': mobile_record[0],
                'speakerpoints': mobile_record[1],
                'ram_storagepoints': mobile_record[2],
                'displaypoints': mobile_record[3],
                'batterypoints': mobile_record[4],
                'totalpoints': mobile_record[5],
                'phoneid': mobile_record[6],
                'deviceid': mobile_record[7],
            }
            total_data.append(temp_json)
        return total_data


    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)



def get_data_and_phone_ids_according_to_pref(
        max_value_dict: Dict[str, int],
        filter_conditions: List[str],
        preferences: Dict[str, int]
) -> Tuple[List[str], List[Dict[str, Union[int, str]]]]:
    phone_ids = []
    pref_data = []
    where_condition = ''
    if filter_conditions:
        where_condition = f"AND {' AND '.join(f'({_})' for _ in filter_conditions)}"
    try:
        query_get_data_of_max_ele = f"""SELECT *
                                        FROM mob_scores
                                        WHERE ((socpoints = {max_value_dict["socpoints"]}) OR 
                                        (displaypoints = {max_value_dict["displaypoints"]}) OR 
                                        (ram_storagepoints = {max_value_dict["ram_storagepoints"]}) OR 
                                        (batterypoints = {max_value_dict["batterypoints"]}) OR 
                                        (speakerpoints = {max_value_dict["speakerpoints"]})) {where_condition};"""
        cursor.execute(query_get_data_of_max_ele)
        mobile_records = cursor.fetchall()
        for mobile_record in mobile_records:
            temp_json = {
                'socpoints': mobile_record[0],
                'speakerpoints': mobile_record[1],
                'ram_storagepoints': mobile_record[2],
                'displaypoints': mobile_record[3],
                'batterypoints': mobile_record[4],
                'totalpoints': mobile_record[5],
                'phoneid': mobile_record[6],
                'deviceid': mobile_record[7],
            }
            pref_data.append(temp_json)
            for preference, preference_points in preferences.items():
                if temp_json[preference] == max_value_dict[preference]:
                    temp_json['totalpoints'] += preference_points
            phone_ids.append(temp_json['phoneid'])
        return phone_ids, pref_data


    except (Exception, psycopg2.Error) as error:

        print("Error while fetching data from PostgreSQL", error)
        print("/n")
        print("Heloooooooooooo")


def get_phone_data_by_id(phone_id):
    # TODO:Implement This
    pass


def main():
    pref = {
        'socpoints': 5,
        'speakerpoints': 1,
        'displaypoints': 4,
        'batterypoints': 3,
        'ram_storagepoints': 2
    }
    total_data, phone_ids = get_all_data_with_preferences(pref)
    pprint(total_data)
    # for i in total_data:
    #     print(i["totalpoints"])
    # print(total_data[0])
    # print(get_max_values(condi))
    # print(len(total_data))


if __name__ == '__main__':
    main()
