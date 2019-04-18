#!/usr/bin/env python

# Copyright 2016 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# biggraph.py
# Created by Eric Bridgeford on 2017-07-13.
# Email: ebridge2@jhu.edu

from __future__ import print_function
import warnings

warnings.simplefilter("ignore")
from itertools import combinations
from collections import defaultdict
import numpy as np
import networkx as nx
import nibabel as nb
import ndmg
import time
import pyximport

try:
    from ndmg.graph.zindex import XYZMorton
except:
    pyximport.install()
    from ndmg.graph.zindex import XYZMorton
import os


class biggraph(object):
    def __init__(self):
        """
        Initializes the fiber graph.
        """
        self.g = nx.Graph(name="Generated by NeuroData's MRI Graphs (ndmg)",
                          version=ndmg.version,
                          date=time.asctime(time.localtime()),
                          source="http://m2g.io",
                          region="brain",
                          sensor="Diffusion MRI",
                          )
        self.edge_dict = defaultdict(int)
        pass

    def make_graph(self, streamlines, attr=None):
        """
        Takes streamlines and produces a graph

        **Positional Arguments:**

                streamlines:
                    - Fiber streamlines either file or array in a dipy EuDX
                      or compatible format.
        """
        nlines = np.shape(streamlines)[0]
        print("# of Streamlines: " + str(nlines))

        print_id = np.max((int(nlines * 0.05), 1))  # in case nlines*.05=0
        for idx, streamline in enumerate(streamlines):
            if (idx % print_id) == 0:
                print(idx)

            points = np.round(streamline).astype(int)
            p = set()
            for point in points:
                try:
                    loc = XYZMorton(tuple(point))
                except IndexError:
                    pass
                else:
                    pass

                if loc:
                    p.add(loc)

            edges = combinations(p, 2)
            for edge in edges:
                # use string here for overflow issues
                lst = tuple([str(node) for node in edge])
                self.edge_dict[tuple(sorted(lst))] += 1

        self.edge_list = [(k[0], k[1], v) for k, v in self.edge_dict.items()]
        pass

    def get_graph(self):
        """
        Returns the graph object created
        """
        try:
            return self.g
        except AttributeError:
            print("Error: the graph has not yet been defined.")
            pass

    def save_graph(self, graphname):
        """
        Saves the graph to disk

        **Positional Arguments:**

                graphname:
                    - Filename for the graph
        """
        sep = '\n'
        with open(graphname, 'w') as edgefile:
            for edge in self.edge_list:
                line = "{} {} {}".format(edge[0], edge[1], edge[2])
                edgefile.write(line + sep)
        pass

    def summary(self):
        """
        User friendly wrapping and display of graph properties
        """
        print("\n Graph Summary:")
        print(nx.info(self.g))
        pass
