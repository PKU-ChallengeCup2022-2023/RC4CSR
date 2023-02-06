from Recommendation.models import Book
with open('data/book_info_all.txt', encoding='utf-8') as fd:
    for line in fd:
        data_list = line.rstrip('\n').split(',')
        Book.objects.create(
            book_tag = int(data_list[0]),
            url = data_list[3],
            bookname = data_list[4],
            author = data_list[5],
            publisher = data_list[6],
            publish_time = data_list[7],
            score = float(data_list[8]),
            comment_num = int(data_list[9]),
            percent_5 = float(data_list[10].rstrip('%')) / 100,
            percent_4 = float(data_list[11].rstrip('%')) / 100,
            percent_3 = float(data_list[12].rstrip('%')) / 100,
            percent_2 = float(data_list[13].rstrip('%')) / 100,
            percent_1 = float(data_list[14].rstrip('%')) / 100
        )
