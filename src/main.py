#! /Users/audrius/Documents/VCSPython/py_scrape/bin/python3

from scrape_aruodas import scrape_data, compare_dataframes
from db_table_aruodas import DBTable


def main():
    data_table = DBTable()
    data_table.create_table()
    has_data = data_table.has_data()
    # data_table.drop_table()
    # data_table.delete_all()
    if not has_data:
        scraped_data = scrape_data()
        data_table.insert_data(scraped_data)
        db_data = data_table.select_all()
        print('\nInitial Table Data:')
        for row in db_data:
            print(row)
    else:
        db_data = data_table.select_all()
        scraped_data = scrape_data()
        data_to_insert = compare_dataframes(scraped_data, db_data)
        data_table.insert_data(data_to_insert)
        data_table.update_discount('Vilnius')
        db_data_updated = data_table.select_all()
        print('\nAppended Table Data:')
        for row in db_data_updated:
            print(row)


if __name__ == "__main__":
    main()
