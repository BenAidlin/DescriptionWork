from ExtractDetailsFromScene import ExtractDetailsFromScene
from csvImport import read_csv_atomic, read_csv_event2mind, import_csv_from_all_files


def extract_single_scene_excel(film_imdb, scene_num, dest="", to_print=False):
    if to_print:
        print("Extracting scene number " + str(scene_num) + ", please wait...")
    exfs = ExtractDetailsFromScene(film_imdb, scene_num)
    exfs.ExtractDetails()
    exfs.exportExcel(dest + str(filmIMDB) + "\\")


def extract_full_film_excel(film_imdb, dest="", to_print=False):
    exfs = ExtractDetailsFromScene(filmIMDB, 1)  # just to get the relevant member for next loop
    for i in range(len(exfs.mg.clip_graphs)):
        if i in exfs.mg.clip_graphs.keys():
            extract_single_scene_excel(film_imdb, i, dest=dest, to_print=to_print)
        else:
            print(str(i) + ' -------> No clipGraph found')


filmIMDB = 'tt0988595'  # 27 dresses
path = "C:\\Users\\USER\\Desktop\\"


extract_full_film_excel(film_imdb=filmIMDB, dest=path, to_print=True)

"""
prefix = "..//..//Automated commonsense reasoning//"
list_of_paths = [prefix + "atomic//v4_atomic_all_agg.csv", prefix + "atomic//v4_atomic_all.csv",
                 prefix + "atomic//v4_atomic_dev.csv", prefix + "atomic//v4_atomic_trn.csv",
                 prefix + "atomic//v4_atomic_tst.csv", prefix + "event2mind//dev.csv", prefix + "event2mind//test.csv",
                 prefix + "event2mind//train.csv"]

# import_csv_from_all_files(list_of_paths, 5)
"""
