
def sorted_by_keys(data):
    data = {
        key: value
        for key, value in sorted(data.items(), key=lambda x: x[0])
    }
    for key, sub_data in data.items():
        data[key] = {
            sub_key: value
            for sub_key, value in sorted(sub_data.items(), key=lambda x: x[0])
        }
    return data
