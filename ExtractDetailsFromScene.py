import pickle
import pandas as pd

"""
using graphClasses, and the pickle should be in the same directory
"""


class ExtractDetailsFromScene:
    def __init__(self, filmIMDB, clip_num):
        annotation_dir = "2017-11-02-51-7637_py3.pkl"
        with open(annotation_dir, 'rb') as fid:
            all_mg = pickle.load(fid, encoding='latin1')
            # latin1 is important here
        self.filmIMDB = filmIMDB
        self.clip_num = clip_num
        self.mg = all_mg[filmIMDB]
        self.clip_num = clip_num
        self.rel_df = pd.DataFrame(
            {'PersonX': [], 'Relationship': [], 'PersonY': [], 'Topic': [], 'Reason': [], 'Time': []})
        self.int_df = pd.DataFrame(
            {'PersonX': [], 'Interaction': [], 'PersonY': [], 'Topic': [], 'Reason': [], 'Time': []})
        self.sum_df = pd.DataFrame(
            {'PersonX': [], 'Summary': [], 'PersonY': [], 'Topic': [], 'Reason': [], 'Time': []})
        self.attribute_df = pd.DataFrame({'Person': [], 'Attribute': [], 'Topic': [], 'Reason': [], 'Time': []})

    def bi_direct_graph(self):
        """
        using this to find nodes that are incorrectly directed
        do this only after finding all interactions\relationships\attributes...
        """
        for n1 in self.mg.clip_graphs[self.clip_num].G.nodes():
            for n2 in self.mg.clip_graphs[self.clip_num].G.nodes():
                if n1 in self.mg.clip_graphs[self.clip_num].G.adj[n2].keys():
                    self.mg.clip_graphs[self.clip_num].G.add_edge(n1, n2)

    def getFullDescription(self):
        return self.mg.clip_graphs[self.clip_num].description

    def twoExtractHelper(self, dead, typ):
        """
        helper function for twoEntitiesExtract, avoiding code duplication
        """
        for i in self.mg.clip_graphs[self.clip_num].find_all_triplets(int_or_rel=typ):
            if i[1] in dead:
                continue
            entity1 = self.mg.clip_graphs[self.clip_num].node_name(i[0])
            interact = self.mg.clip_graphs[self.clip_num].node_name(i[1])
            entity2 = self.mg.clip_graphs[self.clip_num].node_name(i[2])
            topic = 'N/A'
            reason = 'N/A'
            time = 'N/A'
            for n in self.mg.clip_graphs[self.clip_num].G.adj[i[1]].keys():
                if self.mg.clip_graphs[self.clip_num].node_type(n, 'topic') or\
                        self.mg.clip_graphs[self.clip_num].node_type(n, 'attribute'):
                    topic = self.mg.clip_graphs[self.clip_num].node_name(n)
                    dead.append(n)
            for n in self.mg.clip_graphs[self.clip_num].G.adj[i[1]].keys():
                if self.mg.clip_graphs[self.clip_num].node_type(n, 'reason'):
                    reason = self.mg.clip_graphs[self.clip_num].node_name(n)
                    dead.append(n)
            for n in self.mg.clip_graphs[self.clip_num].G.adj[i[1]].keys():
                if self.mg.clip_graphs[self.clip_num].node_type(n, 'time'):
                    time = self.mg.clip_graphs[self.clip_num].node_name(n)
                    dead.append(n)
            dead.append(i[1])
            return [entity1, interact, entity2, topic, reason, time]

    def twoEntitiesExtract(self, dead):
        """
        Extract details using Graph_classes.find_all_triplets
        this does a great work but unfortunately not perfect
        """
        data = self.twoExtractHelper(dead, 'relationship')
        if data is not None:
            self.rel_df = self.rel_df.append({'PersonX': data[0], 'Relationship': data[1], 'PersonY': data[2],
                                              'Topic': data[3], 'Reason': data[4], 'Time': data[5]}, ignore_index=True)
        data = self.twoExtractHelper(dead, 'interaction')
        if data is not None:
            self.int_df = self.int_df.append({'PersonX': data[0], 'Interaction': data[1], 'PersonY': data[2],
                                              'Topic': data[3], 'Reason': data[4], 'Time': data[5]}, ignore_index=True)
        data = self.twoExtractHelper(dead, 'summary')
        if data is not None:
            self.sum_df = self.sum_df.append({'PersonX': data[0], 'Summary': data[1], 'PersonY': data[2],
                                              'Topic': data[3], 'Reason': data[4], 'Time': data[5]}, ignore_index=True)

    def oneEntityExtract(self, dead):
        """
        extract details by going over one person at a time
        """
        df = None
        for n1 in self.mg.clip_graphs[self.clip_num].G.nodes():
            if self.mg.clip_graphs[self.clip_num].node_type(n1, 'entity'):
                entity = self.mg.clip_graphs[self.clip_num].node_name(n1)
                for n2 in self.mg.clip_graphs[self.clip_num].G.adj[n1].keys():
                    if n2 not in dead:
                        df = self.mg.clip_graphs[self.clip_num].node_type(n2)
                    else:
                        continue
                    attribute = self.mg.clip_graphs[self.clip_num].node_name(n2)
                    topic = 'N/A'
                    reason = 'N/A'
                    time = 'N/A'
                    entity2 = 'N/A'
                    for n in self.mg.clip_graphs[self.clip_num].G.adj[n2].keys():
                        if self.mg.clip_graphs[self.clip_num].node_type(n, 'topic') or \
                                self.mg.clip_graphs[self.clip_num].node_type(n, 'attribute'):
                            if topic == 'N/A':
                                topic = self.mg.clip_graphs[self.clip_num].node_name(n)
                            else:
                                topic += self.mg.clip_graphs[self.clip_num].node_name(n)
                            dead.append(n)
                        elif self.mg.clip_graphs[self.clip_num].node_type(n, 'reason'):
                            reason = self.mg.clip_graphs[self.clip_num].node_name(n)
                            dead.append(n)
                        elif self.mg.clip_graphs[self.clip_num].node_type(n, 'time'):
                            time = self.mg.clip_graphs[self.clip_num].node_name(n)
                            dead.append(n)
                        elif self.mg.clip_graphs[self.clip_num].node_type(n, 'entity'):
                            entity2 = self.mg.clip_graphs[self.clip_num].node_name(n)
                            dead.append(n)
                        else:
                            print("located lost node, from: " +
                                  self.mg.clip_graphs[self.clip_num].node_type(n2))
                            print("lost node: " +
                                  self.mg.clip_graphs[self.clip_num].node_name(n) + ":" +
                                  self.mg.clip_graphs[self.clip_num].node_name(n))

                    if df == 'attribute':
                        self.attribute_df = self.attribute_df.append(
                            {'Person': entity, 'Attribute': attribute, 'Topic': topic,
                             'Reason': reason, 'Time': time}, ignore_index=True)
                        dead.append(n2)
                    elif df == 'summary':
                        self.sum_df = self.sum_df.append(
                            {'PersonX': entity, 'Summary': attribute, 'PersonY': entity2,
                             'Topic': topic, 'Reason': reason, 'Time': time},
                            ignore_index=True)
                        dead.append(n2)
                    elif df == 'relationship':
                        self.rel_df = self.rel_df.append(
                            {'PersonX': entity, 'Relationship': attribute, 'PersonY': entity2,
                             'Topic': topic, 'Reason': reason, 'Time': time}, ignore_index=True)
                        dead.append(n2)
                    elif df == 'interaction' or df == 'action':
                        self.int_df = self.int_df.append(
                            {'PersonX': entity, 'Interaction': attribute, 'PersonY': entity2,
                             'Topic': topic, 'Reason': reason, 'Time': time}, ignore_index=True)
                        dead.append(n2)

                dead.append(n1)

    def ExtractDetails(self):
        """
        search for all nodes and relations, than, bi-direct graph and search again.
        i do this because some relations are embedded the wrong direction, but don't do this
        from start so that personX and personY will not flip when its unnecessary.
        """
        dead = []

        self.twoEntitiesExtract(dead)
        self.oneEntityExtract(dead)
        self.bi_direct_graph()
        self.twoEntitiesExtract(dead)
        self.oneEntityExtract(dead)

        self.attribute_df.sort_values(by='Time', inplace=True)
        self.attribute_df.reset_index(inplace=True, drop=True)
        self.int_df.sort_values(by='Time', inplace=True)
        self.int_df.reset_index(inplace=True, drop=True)
        self.sum_df.sort_values(by='Time', inplace=True)
        self.sum_df.reset_index(inplace=True, drop=True)
        self.rel_df.sort_values(by='Time', inplace=True)
        self.rel_df.reset_index(inplace=True, drop=True)
        for n in self.mg.clip_graphs[self.clip_num].G.nodes():
            if n not in dead:
                if not self.mg.clip_graphs[self.clip_num].node_type(n, 'scene') and \
                        not self.mg.clip_graphs[self.clip_num].node_type(n, 'situation'):
                    print("!!! Warning !!! - not all data was extracted")
                    print("=== missing node: ===")
                    print(self.mg.clip_graphs[self.clip_num].node_type(n) + ": " +
                          self.mg.clip_graphs[self.clip_num].node_name(n))
                    print("nodes connected to him:")
                    for n2 in self.mg.clip_graphs[self.clip_num].G.nodes():
                        if n in self.mg.clip_graphs[self.clip_num].G.adj[n].keys() \
                                or n2 in self.mg.clip_graphs[self.clip_num].G.adj[n].keys():
                            print(self.mg.clip_graphs[self.clip_num].node_type(n2) + ": " +
                                  self.mg.clip_graphs[self.clip_num].node_name(n2))

    def exportExcel(self, path=''):
        """
        this will create one excel file for the scene that will contain 4 sheets, one for each df
        file name will be formatted <filmIMDB>_<scene_number>.xlsx
        the file will be located at path
        """
        writer = pd.ExcelWriter(path + self.filmIMDB + '_' + str(self.clip_num) + '.xlsx', engine='xlsxwriter')
        self.int_df.to_excel(writer, 'interactions')
        self.sum_df.to_excel(writer, 'summaries')
        self.attribute_df.to_excel(writer, 'attributes')
        self.rel_df.to_excel(writer, 'relationships')
        writer.save()
