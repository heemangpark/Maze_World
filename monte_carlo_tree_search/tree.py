import numpy as np
import networkx as nx

from env.maze_func import get_avail_action, terminated
from monte_carlo_tree_search.tree_functions import expand, children, select, backup


class Tree:
    def __init__(self, maze, agent_id=0, init_locs=np.array([[7, 0], [6, 7]])):
        self.g = nx.DiGraph()
        self.g.add_node(1, state=init_locs[agent_id], N=1)
        self.maze = maze
        self.action_sequence = []
        self.init_loc = init_locs[agent_id]
        self.state_sequence = [self.init_loc]

        _ = expand(1, self.g, get_avail_action(maze, init_locs[agent_id]))

    def grow(self):
        while True:
            self.state_sequence = [self.init_loc]
            idx, self.action_sequence = 1, []
            """selection"""
            while len(children(idx, self.g)) != 0:
                idx, a = select(idx, self.g)
                self.action_sequence.append(a)
                curr_state = self.g.nodes[idx]['state']
                self.state_sequence.append(curr_state)

            """terminal check on selected leaf"""
            if terminated(self.maze, self.g.nodes[idx]['state']):
                break
            else:
                pass

            """expansion"""
            curr_state = self.g.nodes[idx]['state']
            leaves = expand(idx, self.g, avail_actions=get_avail_action(self.maze, curr_state))
            """backup"""
            for leaf in leaves:
                backup(leaf, self.g)

    def route(self):
        return self.action_sequence

# def grow(self):
#     node_idx = 1
#     while self.g.nodes[node_idx]['state'] != TO:
#         prev_state = self.g.nodes[node_idx]['state']
#         node_idx, action = select(node_idx, self.g)
#         self.action_sequence.append(action)
#         next_state = transition(prev_state, action)
#         self.maze = State(next_state)
#         # print("took action \"{}\" from {} & now at {}".format(action, prev_state, next_state))
#         leaves = expand(node_idx, self.g)
#         for leaf in leaves:
#             sr = simulated_reward(self.g.nodes[leaf]['state'], 10)
#             backup(leaf, self.g, sr)
