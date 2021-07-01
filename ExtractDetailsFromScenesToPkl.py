from ExtractDetailsFromScene import ExtractDetailsFromScene
import pandas as pd
import os

films = ['tt0037884', 'tt0068646', 'tt0073486', 'tt0097576', 'tt0100405', 'tt0106918', 'tt0108160',
         'tt0109830', 'tt0109831', 'tt0110912', 'tt0116695', 'tt0118715', 'tt0118842', 'tt0119822',
         'tt0147800', 'tt0167404', 'tt0212338', 'tt0240772', 'tt0241527', 'tt0286106', 'tt0375679',
         'tt0388795', 'tt0416320', 'tt0455824', 'tt0467406', 'tt0478311', 'tt0790636', 'tt0822832',
         'tt0970416', 'tt0988595', 'tt1010048', 'tt1045658', 'tt1142988', 'tt1189340', 'tt1193138',
         'tt1285016', 'tt1385826', 'tt1454029', 'tt1499658', 'tt1568346', 'tt1570728', 'tt1632708',
         'tt1798709', 'tt1907668', 'tt2267998']

for film in films:
    try:
        os.mkdir('C:\\Users\\USER\\Desktop\\films\\pkl_dataframes\\' + film)
    except:
        pass
    exfs = ExtractDetailsFromScene(film, 1)
    for scene in exfs.mg.clip_graphs.keys():
        exfs = ExtractDetailsFromScene(film, scene)
        exfs.ExtractDetails()
        exfs.exportPkl('C:\\Users\\USER\\Desktop\\films\\pkl_dataframes\\' + film + '\\')
