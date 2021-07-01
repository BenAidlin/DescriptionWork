import os
import pickle
import pandas as pd
import difflib
import timeit


class RuleImplementationPerFile:
    def __init__(self, pickle_rules_path, pickle_scene_path):
        file = open(pickle_rules_path, 'rb')
        automated_reasoning = pickle.load(file)
        file.close()
        self.atomic = automated_reasoning[0:5]
        self.e2m = automated_reasoning[5:8]
        file = open(pickle_scene_path, 'rb')
        self.df = pickle.load(file)
        file.close()
        self.results = pd.DataFrame(
            {'Event': [], 'PersonX': [], 'PersonY': [], 'xIntent': [], 'xEmotion': [], 'xWant': [],
             'xReact': [], 'xNeed': [], 'xEffect': [], 'xAttribute': [], 'oEmotion': [],
             'oWant': [], 'oReact': [], 'oEffect': []})

    def implement_scene(self):
        for index, row in self.df.iterrows():
            person_x = row['PersonX']
            if person_x == 'N/A': person_x = ""
            person_y = row['PersonY']
            topic = row['Topic']
            reason = row['Reason']
            try:
                interaction = row['Interaction']
            except:
                interaction = row['Summary']
            if interaction == 'N/A': interaction = ""
            if topic == 'N/A': topic = ""
            if reason == 'N/A': reason = ""
            if person_y == 'N/A':
                person_y = ""
                event = "PersonX " + interaction + ", " + topic + " " + reason
            else:
                event = "PersonX " + interaction + " PersonY " + topic + " " + reason
            action = interaction.split()[0]
            dic = {'Event': event, 'PersonX': person_x, 'PersonY': person_y,
                   'xIntent': [], 'xEmotion': [],
                   'xWant': [], 'xReact': [],
                   'xNeed': [], 'xEffect': [],
                   'xAttribute': [], 'oEmotion': [],
                   'oWant': [], 'oReact': [],
                   'oEffect': []}

            for em in self.e2m:
                for k in em.keys():
                    start = timeit.default_timer()

                    euq = 13  # self.lc.getEuqlidianDiff()
                    dflib_sqmtch = difflib.SequenceMatcher(None, event, k).ratio()
                    action_found = action in k.split()

                    if action in k.split() and difflib.SequenceMatcher(None, event, k).ratio() > 0.72:
                        end = timeit.default_timer()
                        # print(start-end)
                        print(event)
                        print(k)
                        dic['xIntent'].append(em[k][1])
                        dic['xEmotion'].append(em[k][2])
                        dic['oEmotion'].append(em[k][3])

            for at in self.atomic:
                for k in at.keys():

                    dflib_sqmtch = difflib.SequenceMatcher(None, event, k).ratio()
                    action_found = action in k.split()

                    if action in k.split() and difflib.SequenceMatcher(None, event, k).ratio() > 0.72:
                        print(event)
                        print(k)
                        dic['xIntent'].append(at[k][5])
                        dic['xWant'].append(at[k][8])
                        dic['xReact'].append(at[k][7])
                        dic['xNeed'].append(at[k][6])
                        dic['xEffect'].append(at[k][4])
                        dic['xAttribute'].append(at[k][3])
                        dic['oWant'].append(at[k][2])
                        dic['oReact'].append(at[k][1])
                        dic['oEffect'].append(at[k][0])

            self.results = self.results.append(dic, ignore_index=True)

    def extract_results(self, path):
        self.results.to_csv(path)


class RuleImplementationPerFilm:
    def __init__(self, pickle_scene_folder, pickle_rules_path, dest, film_imdb, scene_num):
        self.pickle_scene_folder = pickle_scene_folder
        self.pickle_rules_path = pickle_rules_path
        self.dest = dest
        self.imdb = film_imdb
        self.scene_num = scene_num

    def implement_all(self):
        p1 = self.pickle_rules_path
        for i in range(self.scene_num):  # film scene amount
            p2 = self.pickle_scene_folder + self.imdb + '_' + str(i) + '_interaction.pkl'
            p3 = self.pickle_scene_folder + self.imdb + '_' + str(i) + '_summary.pkl'
            try:
                sri = RuleImplementationPerFile(p1, p2)
                sri.implement_scene()
                sri.extract_results(self.dest + self.imdb + '_' + str(i) + '_interaction_results.csv')
                sri = RuleImplementationPerFile(p1, p3)
                sri.implement_scene()
                sri.extract_results(self.dest + self.imdb + '_' + str(i) + '_summary_results.csv')
            except FileNotFoundError:
                print("scene number " + str(i) + " not found")


"""
pick1 = "automated_reasoning_rules.txt"
pickabs = 'C:\\Users\\USER\\Desktop\\films\\pkl_dataframes\\tt0988595\\'


#implement single scene
ri = RuleImplementationPerFile(pick1, pick2)
ri.implement_scene()
ri.extract_results("C:\\Users\\USER\\Desktop\\here.csv")

# implement whole film
dest_dir = "C:\\Users\\USER\\Desktop\\Results_2\\"
fri = RuleImplementationPerFilm(pickabs, pick1, dest_dir, 'tt0988595', 314)
fri.implement_all()
"""

base_dir = "C:\\Users\\USER\\Desktop\\Results for all films using difflib.SequenceMatcher\\"
base_pick = "C:\\Users\\USER\\Desktop\\films\\pkl_dataframes\\"
films = ['tt0037884', 'tt0068646', 'tt0073486', 'tt0097576', 'tt0100405', 'tt0106918', 'tt0108160',
         'tt0109830', 'tt0109831', 'tt0110912', 'tt0116695', 'tt0118715', 'tt0118842', 'tt0119822',
         'tt0147800', 'tt0167404', 'tt0212338', 'tt0240772', 'tt0241527', 'tt0286106', 'tt0375679',
         'tt0388795', 'tt0416320', 'tt0455824', 'tt0467406', 'tt0478311', 'tt0790636', 'tt0822832',
         'tt0970416', 'tt0988595', 'tt1010048', 'tt1045658', 'tt1142988', 'tt1189340', 'tt1193138',
         'tt1285016', 'tt1385826', 'tt1454029', 'tt1499658', 'tt1568346', 'tt1570728', 'tt1632708',
         'tt1798709', 'tt1907668', 'tt2267998']
automated_reasoning_rules = "automated_reasoning_rules.txt"
for film_imdb in films:
    try:
        os.mkdir(base_dir+film_imdb)
    except:
        pass
    fri = RuleImplementationPerFilm(base_pick+film_imdb+"\\", automated_reasoning_rules, base_dir+film_imdb+"\\", film_imdb,
                                    400)  # all films have less than 400 scenes, the module will catch the exception.
    fri.implement_all()

