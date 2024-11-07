from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Page:
  # Dataclass weil man dort einfach die Attribute ohne init deklarieren muss 
    name: str
    rank: float = 1.0
    links_to: List[str] = field(default_factory=list)
    links_from: List[str] = field(default_factory=list)


class PageRank:
    def __init__(self, pages: List[Page], damping_factor: float = 0.85, max_iterations: int = 100):
        self.pages: List[Page] = pages
        self.damping_factor: float = damping_factor
        self.max_iterations: int = max_iterations

        for page in self.pages:
            for page_to in page.links_to:
                target_page = self.get_page_by_name(page_to)
                if target_page:
                    target_page.links_from.append(page.name)
    
    def calculate_ranks(self):
        for page in self.pages:
            page.rank = 1 - self.damping_factor + self.damping_factor * self.get_reference_ranks(page.name)

    def get_reference_ranks(self, page_name: str) -> float:
        rank: float = 0
        for page in self.pages:
            if page.name != page_name:
                if page_name in page.links_to:
                    rank += page.rank / len(page.links_to)
        return rank

    def get_page_by_name(self, page_name: str) -> Page | None:
        return next((page for page in self.pages if page.name == page_name), None)
    
    def run(self):
        for _ in range(self.max_iterations):
            self.calculate_ranks()

    def get_ranks(self) -> Dict[str, float]:
        return {page.name: round(page.rank, 2) for page in self.pages}


def analyze_graph(graph: List[Page], graph_name: str, damping_factor: float = 0.85, max_iterations: int = 1000) -> Dict[str, float]:
    pr = PageRank(graph, damping_factor, max_iterations)
    pr.run()
    ranks = pr.get_ranks()
    print(f'Graph {graph_name}:', ranks)
    return ranks

graph1: List[Page] = [
    Page('A', links_to=['B']),
    Page('B', links_to=['A']),
]

graph2: List[Page] = [
    Page('A', links_to=['C']),
    Page('B', links_to=['A']),
    Page('C', links_to=['B'])
]

graph3: List[Page] = [
    Page('A', links_to=['B','C']),
    Page('B', links_to=['A','C']),
    Page('C', links_to=[])
]

graph4: List[Page] = [
    Page('A', links_to=['B']),
    Page('B', links_to=['C']),
    Page('C', links_to=[]),
]

graphs = {
    "1": graph1,
    "2": graph2,
    "3": graph3,
    "4": graph4
}

results = {name: analyze_graph(graph, name) for name, graph in graphs.items()}