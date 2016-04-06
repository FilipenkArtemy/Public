from bs4 import BeautifulSoup


def build_graph(path):
    soup = BeautifulSoup(open(path))
    graph = {a: [] for a in range(1, 617)}
    q = 1
    for tag in soup.find_all('a'):
        if tag.get('name', '').startswith('n_'):
            q = int(tag['name'][2:])
        if tag.get('href', '').startswith('#n_'):
            graph[q].append(int(tag['href'][3:]))
    with open('graph.dot', 'w') as f:
        f.write('digraph G {\n')
        for i in graph.keys():
            for q in graph[i]:
                f.write(str(i) + '->' + str(q)+'\n')
        f.write('}')
