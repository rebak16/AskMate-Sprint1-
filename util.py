import connection


def get_next_id(filename):
    list_of_datas = connection.read_csv(filename)
    return str(int(list_of_datas[-1]['id']) + 1)