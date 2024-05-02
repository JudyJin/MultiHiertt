from table_description_generation_new import *
import os

def main():
    # input_dev = json.load(open("dev.json"))
    # save = []
    # for i, inp in enumerate(input_dev):
    #     table_descriptions = {}
    #     tables = inp['tables']
    #     for i, table in enumerate(tables):
    #         data, header, top_header_nonexist_flag = readHTML(table)
    #         table_description = generateDescription(data, header, top_header_nonexist_flag)
    #         for key, value in table_description.items():
    #             table_descriptions[str(i)+"-"+key] = value
    #     inp['table_description'] = table_descriptions
    #     save.append(inp)

    # with open("dev_new.json", "w") as f:
    #     json.dump(save, f)

    input_dev = json.load(open("train.json"))
    save = []
    for i, inp in enumerate(input_dev):
        table_descriptions = {}
        tables = inp['tables']
        for i, table in enumerate(tables):
            data, header, top_header_nonexist_flag = readHTML(table)
            table_description = generateDescription(data, header, top_header_nonexist_flag)
            for key, value in table_description.items():
                table_descriptions[str(i)+"-"+key] = value
        inp['table_description'] = table_descriptions
        save.append(inp)

    with open("train_new.json", "w") as f:
        json.dump(save, f)

    input_dev = json.load(open("test.json"))
    save = []
    for i, inp in enumerate(input_dev):
        table_descriptions = {}
        tables = inp['tables']
        for i, table in enumerate(tables):
            data, header, top_header_nonexist_flag = readHTML(table)
            table_description = generateDescription(data, header, top_header_nonexist_flag)
            for key, value in table_description.items():
                table_descriptions[str(i)+"-"+key] = value
        inp['table_description'] = table_descriptions
        save.append(inp)

    with open("test_new.json", "w") as f:
        json.dump(save, f)

if __name__ == "__main__":
    main()