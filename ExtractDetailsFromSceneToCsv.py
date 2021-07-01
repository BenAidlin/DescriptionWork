from ExtractDetailsFromScene import ExtractDetailsFromScene
import pandas as pd
import os

# part 1 - extracting the films info from graphClasses to csv files


def extract_single_scene_excel(exfs, scene_num, dest="", to_print=False):
    if to_print:
        print("Extracting scene number " + str(scene_num) + " from " + str(exfs.filmIMDB) + ", please wait...")
    exfs.ExtractDetails()
    exfs.exportExcel(dest + str(exfs.filmIMDB) + "\\")


def extract_full_film_excel(film_imdb, dest="", to_print=False, path_to_scenes_gt="", path_to_video_events=""):
    try:
        os.mkdir(dest+film_imdb)
    except:
        pass
    scenes_time = pd.DataFrame({'Scene': [], 'Start time': [], 'End time': []})
    char_time = pd.DataFrame({'Character': [], 'Total time': []})
    exfs = ExtractDetailsFromScene(film_imdb, 1)  # just to get the relevant member for next loop
    character_scene_time = {}
    for i in range(1, len(exfs.mg.clip_graphs)):
        if i in exfs.mg.clip_graphs.keys():
            exfs = ExtractDetailsFromScene(film_imdb, i)
            extract_single_scene_excel(exfs, i, dest=dest, to_print=to_print)
            tup = exfs.getSceneBoundaries(path_to_scenes_gt + exfs.filmIMDB + ".scenes.gt",
                                          path_to_video_events + exfs.filmIMDB + ".videvents")
            curr_time = exfs.getCharacterTime(tup)
            for j in curr_time:
                if j[0] not in character_scene_time.keys():
                    character_scene_time[j[0]] = float(j[2])-float(j[1])
                else:
                    character_scene_time[j[0]] += float(j[2])-float(j[1])
        else:
            print(str(i) + ' -------> No clipGraph found')
            tup = exfs.getSceneBoundaries(path_to_scenes_gt + exfs.filmIMDB + ".scenes.gt",
                                          path_to_video_events + exfs.filmIMDB + ".videvents")
        scenes_time = scenes_time.append({'Scene': i, 'Start time': tup[0], 'End time': tup[1]}, ignore_index=True)
    for i in character_scene_time.keys():
        char_time = char_time.append({'Character': i,'Total time': character_scene_time[i]}, ignore_index=True)
    writer = pd.ExcelWriter(dest + str(film_imdb) + "\\" + film_imdb + '_total_details'
                            + '.xlsx', engine='xlsxwriter')
    char_time.sort_values(ascending=False, by='Total time', inplace=True)
    char_time.reset_index(inplace=True, drop=True)
    scenes_time.to_excel(writer, 'scene boundaries')
    char_time.to_excel(writer, 'character appearance time')
    writer.save()


films = ['tt0037884', 'tt0068646', 'tt0073486', 'tt0097576', 'tt0100405', 'tt0106918', 'tt0108160',
         'tt0109830', 'tt0109831', 'tt0110912', 'tt0116695', 'tt0118715', 'tt0118842', 'tt0119822',
         'tt0147800', 'tt0167404', 'tt0212338', 'tt0240772', 'tt0241527', 'tt0286106', 'tt0375679',
         'tt0388795', 'tt0416320', 'tt0455824', 'tt0467406', 'tt0478311', 'tt0790636', 'tt0822832',
         'tt0970416', 'tt0988595', 'tt1010048', 'tt1045658', 'tt1142988', 'tt1189340', 'tt1193138',
         'tt1285016', 'tt1385826', 'tt1454029', 'tt1499658', 'tt1568346', 'tt1570728', 'tt1632708',
         'tt1798709', 'tt1907668', 'tt2267998']
# filmIMDB = 'tt0988595'  # 27 dresses
dest_path = "C:\\Users\\USER\\Desktop\\"
path_to_scenes_gt = "C:\\Users\\USER\\Desktop\\armins " \
                    "research\\Movie_Graph_Dataset\\mg_videoinfo\\scene_boundaries\\"
path_to_video_events = "C:\\Users\\USER\\Desktop\\armins " \
                       "research\\Movie_Graph_Dataset\\mg_videoinfo\\video_boundaries\\"

for film_imdbi in films:
    try:
        os.mkdir(dest_path+'films_pkl')
    except:
        pass
    finally:
        extract_full_film_excel(film_imdb=film_imdbi, dest=dest_path + 'films\\', to_print=True,
                                path_to_scenes_gt=path_to_scenes_gt, path_to_video_events=path_to_video_events)


# part 2 - extracting the automated reasoning rule-set from csv files to python

from ImportCsvFromReasoningToDict import read_csv_atomic, read_csv_event2mind, import_csv_from_all_files
import pickle
prefix = "..//..//Automated commonsense reasoning//"
list_of_paths = [prefix + "atomic//v4_atomic_all_agg.csv", prefix + "atomic//v4_atomic_all.csv",
                 prefix + "atomic//v4_atomic_dev.csv", prefix + "atomic//v4_atomic_trn.csv",
                 prefix + "atomic//v4_atomic_tst.csv", prefix + "event2mind//dev.csv", prefix + "event2mind//test.csv",
                 prefix + "event2mind//train.csv"]

automated_reasoning = import_csv_from_all_files(list_of_paths, 5)

file = open('automated_reasoning_rules.pkl', 'wb')
pickle.dump(automated_reasoning, file)
file.close()
