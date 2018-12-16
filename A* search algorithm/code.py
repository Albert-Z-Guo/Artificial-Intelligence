from expand import expand
import heapq as minheap

def a_star_search (dis_map, time_map, start, end):
	path = []
	# be sure to call the imported function expand to get the next list of nodes
	open_nodes = []
	closed_nodes = []
	node_expansion_dict = {}
	node_path_dict = {}

	# check if start or end in the map
	if start not in dis_map or end not in dis_map:
		return path

	# initialization
	node = [dis_map[start][end], start]
	minheap.heappush(open_nodes, node)
	node_path_dict[start] = tuple(path)

	while open_nodes[0][1] != end:
		# choose a node with minimum expected cost
		# break ties alphabetically if nodes have the same expected cost
		node = minheap.heappop(open_nodes)
		path = list(node_path_dict[node[1]])
		path.append(node[1])

		# expand this node to get the next list of nodes
		if node[1] in node_expansion_dict:
			next_node_list = node_expansion_dict[node[1]]
		else:
			# if cost of node is not available
			# choose another node with minimum expected cost
			if node[1] not in time_map:
				closed_nodes.append(node[1])
				continue
			next_node_list = expand(node[1], time_map)
			node_expansion_dict[node[1]] = next_node_list

		for next_node in next_node_list:
			# if the expanded node not in closed_nodes
			# and its heuristic cost is available (in dis_map)
			if next_node not in closed_nodes and next_node in dis_map:
				# evaluate total cost
				g_cost = (node[0] - dis_map[node[1]][end]) + time_map[node[1]][next_node]
				h_cost = dis_map[next_node][end]
				total_cost = g_cost + h_cost
				for i in range(len(open_nodes)):
					if next_node == open_nodes[i][1]:
						# if the node's total cost can be updated
						if total_cost < open_nodes[i][0]:
							# update total cost
							open_nodes[i][0] = total_cost
							# update path
							node_path_dict[next_node] = tuple(path)
							# maintain heap structure
							minheap.heapify(open_nodes)
						break
				else:
					# push the expanded node in open_nodes
					minheap.heappush(open_nodes, [total_cost, next_node])
					# if path to the expanded node does not exist
					if next_node not in node_path_dict:
						node_path_dict[next_node] = tuple(path)

		# add used node to closed_nodes
		closed_nodes.append(node[1])
		# if there is nowhere to go before reaching end
		if len(open_nodes) == 0:
			return []

	# append the final node to path
	node = minheap.heappop(open_nodes)
	closed_nodes.append(node[1])
	path = list(node_path_dict[node[1]])
	path.append(node[1])
	return path
