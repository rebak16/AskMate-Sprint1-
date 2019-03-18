import connection


def get_next_id(filename):
    list_of_datas = connection.read_csv(filename)
    sorted_datas = sorted(list_of_datas, key=lambda row: row['id'])
    return str(int(sorted_datas[-1]['id']) + 1)
