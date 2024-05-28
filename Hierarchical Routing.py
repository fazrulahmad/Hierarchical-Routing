import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw_circular_area(G, routers, pos, center, radius, color, label):
    n = len(routers)
    for i, router in enumerate(routers):
        angle = 2 * np.pi * i / n
        pos[router] = (center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle))
        nx.draw_networkx_nodes(G, pos, nodelist=[router], node_size=700, node_color=color)
        nx.draw_networkx_labels(G, pos, labels={router: router})

    circle = plt.Circle(center, radius, color=color, alpha=0.2, zorder=0)
    plt.gca().add_patch(circle)
    plt.text(center[0], center[1], label, horizontalalignment='center', verticalalignment='center', fontsize=12, fontweight='bold')

class Router:
    def __init__(self, name):
        self.name = name
        self.routing_table = {}

    def add_route(self, destination, next_hop):
        self.routing_table[destination] = next_hop

    def get_next_hop(self, destination):
        return self.routing_table.get(destination, None)

    def __repr__(self):
        return f"Router({self.name})"

class Area:
    def __init__(self, area_id):
        self.area_id = area_id
        self.routers = {}

    def add_router(self, router):
        self.routers[router.name] = router

    def get_router(self, router_name):
        return self.routers.get(router_name, None)

    def remove_router(self, router_name):
        if router_name in self.routers:
            del self.routers[router_name]

    def __repr__(self):
        return f"Area({self.area_id})"

class Network:
    def __init__(self):
        self.areas = {}
        self.area_border_routers = {}
        self.G = nx.DiGraph()

    def add_area(self, area):
        self.areas[area.area_id] = area

    def remove_area(self, area_id):
        if area_id in self.areas:
            del self.areas[area_id]
            if area_id in self.area_border_routers:
                del self.area_border_routers[area_id]

    def add_area_border_router(self, router, area_id):
        if area_id not in self.area_border_routers:
            self.area_border_routers[area_id] = []
        self.area_border_routers[area_id].append(router)

    def route_packet(self, source_router_name, destination_router_name):
        source_router = None
        source_area_id = None
        destination_router = None
        destination_area_id = None

        for area_id, area in self.areas.items():
            if source_router_name in area.routers:
                source_router = area.routers[source_router_name]
                source_area_id = area_id
            if destination_router_name in area.routers:
                destination_router = area.routers[destination_router_name]
                destination_area_id = area_id

        if not source_router or not destination_router:
            return None

        if source_area_id == destination_area_id:
            return source_router.get_next_hop(destination_router_name)

        for border_router in self.area_border_routers[source_area_id]:
            next_hop = border_router.get_next_hop(destination_router_name)
            if next_hop:
                return border_router.name, next_hop

        return None

    def visualize_network(self, path=None):
        pos = {}

        # Define areas and their positions
        area_positions = {
            "Region 1": ((0, 4), 1.5),
            "Region 2": ((4, 4), 1.5),
            "Region 3": ((0, 0), 1.5),
            "Region 4": ((4, 0), 1.5),
            "Region 5": ((8, 0), 1.5)
        }
        area_colors = {
            "Region 1": 'red',
            "Region 2": 'green',
            "Region 3": 'blue',
            "Region 4": 'orange',
            "Region 5": 'purple'
        }

        # Draw areas and nodes
        for area_id, (center, radius) in area_positions.items():
            if area_id in self.areas:
                routers = [router.name for router in self.areas[area_id].routers.values()]
                draw_circular_area(self.G, routers, pos, center, radius, area_colors[area_id], area_id)

        # Add edges
        for area in self.areas.values():
            for router in area.routers.values():
                for destination, next_hop in router.routing_table.items():
                    self.G.add_edge(router.name, next_hop)

        nx.draw_networkx_edges(self.G, pos, arrowstyle='->', arrowsize=20)

        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='r', width=2)

        plt.title("Hierarchical Routing Network")
        plt.axis('equal')
        plt.show()

    def add_edge(self, source, destination, weight=1):
        self.G.add_edge(source, destination, weight=weight)

    def shortest_path(self, source, target):
        return nx.shortest_path(self.G, source=source, target=target, weight='weight')

    def print_routing_table(self, router_name):
        for area in self.areas.values():
            if router_name in area.routers:
                router = area.routers[router_name]
                print(f"Routing Table for {router_name}:")
                print(f"Dest\tNext Hop")
                for destination, next_hop in router.routing_table.items():
                    print(f"{destination}\t{next_hop}")

def menu():
    network = Network()

    # Create routers
    router_1a = Router("1A")
    router_1b = Router("1B")
    router_1c = Router("1C")
    router_2a = Router("2A")
    router_2b = Router("2B")
    router_2c = Router("2C")
    router_2d = Router("2D")
    router_3a = Router("3A")
    router_3b = Router("3B")
    router_4a = Router("4A")
    router_4b = Router("4B")
    router_4c = Router("4C")
    router_5a = Router("5A")
    router_5b = Router("5B")
    router_5c = Router("5C")
    router_5d = Router("5D")
    router_5e = Router("5E")

    # Add routes to routers
    router_1a.add_route("1B", "1B")
    router_1a.add_route("1C", "1C")
    router_1a.add_route("2A", "1B")
    router_1a.add_route("2B", "1B")
    router_1a.add_route("2C", "1B")
    router_1a.add_route("2D", "1B")
    router_1a.add_route("3A", "1C")
    router_1a.add_route("3B", "1C")
    router_1a.add_route("4A", "1C")
    router_1a.add_route("4B", "1C")
    router_1a.add_route("4C", "1C")
    router_1a.add_route("5A", "1C")
    router_1a.add_route("5B", "1C")
    router_1a.add_route("5C", "1C")
    router_1a.add_route("5D", "1C")
    router_1a.add_route("5E", "1C")

    router_1b.add_route("1A", "1A")
    router_1b.add_route("1C", "1A")
    router_1b.add_route("2A", "2A")
    router_1b.add_route("2B", "2A")
    router_1b.add_route("2C", "2A")
    router_1b.add_route("2D", "2A")

    router_1c.add_route("1A", "1A")
    router_1c.add_route("1B", "1A")
    router_1c.add_route("3A", "3A")
    router_1c.add_route("3B", "3A")

    router_2a.add_route("2B", "2B")
    router_2a.add_route("2C", "2C")
    router_2a.add_route("2D", "2C")
    router_2a.add_route("1A", "1B")
    router_2a.add_route("1B", "1B")
    router_2a.add_route("1C", "1B")

    router_2b.add_route("2A", "2A")
    router_2b.add_route("2C", "2A")
    router_2b.add_route("2D", "2A")

    router_2c.add_route("2A", "2A")
    router_2c.add_route("2B", "2A")
    router_2c.add_route("2D", "2A")

    router_2d.add_route("2A", "2A")
    router_2d.add_route("2B", "2A")
    router_2d.add_route("2C", "2A")

    router_3a.add_route("3B", "3B")
    router_3a.add_route("1A", "1C")
    router_3a.add_route("1B", "1C")
    router_3a.add_route("1C", "1C")

    router_3b.add_route("3A", "3A")

    router_4a.add_route("4B", "4B")
    router_4a.add_route("4C", "4C")
    router_4a.add_route("1A", "1C")
    router_4a.add_route("1B", "1C")
    router_4a.add_route("1C", "1C")

    router_4b.add_route("4A", "4A")
    router_4b.add_route("4C", "4A")

    router_4c.add_route("4A", "4A")
    router_4c.add_route("4B", "4A")

    router_5a.add_route("5B", "5B")
    router_5a.add_route("5C", "5C")
    router_5a.add_route("5D", "5C")
    router_5a.add_route("5E", "5C")
    router_5a.add_route("1A", "1C")
    router_5a.add_route("1B", "1C")
    router_5a.add_route("1C", "1C")

    router_5b.add_route("5A", "5A")
    router_5b.add_route("5C", "5A")
    router_5b.add_route("5D", "5A")
    router_5b.add_route("5E", "5A")

    router_5c.add_route("5A", "5A")
    router_5c.add_route("5B", "5A")
    router_5c.add_route("5D", "5A")
    router_5c.add_route("5E", "5A")

    router_5d.add_route("5A", "5A")
    router_5d.add_route("5B", "5A")
    router_5d.add_route("5C", "5A")
    router_5d.add_route("5E", "5A")

    router_5e.add_route("5A", "5A")
    router_5e.add_route("5B", "5A")
    router_5e.add_route("5C", "5A")
    router_5e.add_route("5D", "5A")

    # Create areas and add routers
    area_1 = Area("Region 1")
    area_1.add_router(router_1a)
    area_1.add_router(router_1b)
    area_1.add_router(router_1c)

    area_2 = Area("Region 2")
    area_2.add_router(router_2a)
    area_2.add_router(router_2b)
    area_2.add_router(router_2c)
    area_2.add_router(router_2d)

    area_3 = Area("Region 3")
    area_3.add_router(router_3a)
    area_3.add_router(router_3b)

    area_4 = Area("Region 4")
    area_4.add_router(router_4a)
    area_4.add_router(router_4b)
    area_4.add_router(router_4c)

    area_5 = Area("Region 5")
    area_5.add_router(router_5a)
    area_5.add_router(router_5b)
    area_5.add_router(router_5c)
    area_5.add_router(router_5d)
    area_5.add_router(router_5e)

    # Add areas to network
    network.add_area(area_1)
    network.add_area(area_2)
    network.add_area(area_3)
    network.add_area(area_4)
    network.add_area(area_5)

    # Add edges to the graph for shortest path calculation
    for area in network.areas.values():
        for router in area.routers.values():
            for destination, next_hop in router.routing_table.items():
                network.add_edge(router.name, next_hop)

    while True:
        print("\nMenu:")
        print("1. Shortest path")
        print("2. Tampilkan tabel hierarchical routing")
        print("3. Tambah Region")
        print("4. Hapus Region")
        print("5. Exit")
        choice = input("Pilih opsi: ")

        if choice == '1':
            source = input("Masukkan router sumber: ")
            destination = input("Masukkan router tujuan: ")
            try:
                path = network.shortest_path(source, destination)
                print(f"Rute terpendek dari {source} ke {destination}: {' -> '.join(path)}")
                network.visualize_network(path)
            except nx.NetworkXNoPath:
                print(f"Tidak ada rute dari {source} ke {destination}.")
        elif choice == '2':
            router_name = input("Masukkan nama router: ")
            network.print_routing_table(router_name)
        elif choice == '3':
            region_name = input("Masukkan nama region: ")
            num_routers = int(input("Masukkan jumlah router dalam region: "))
            new_area = Area(region_name)
            for _ in range(num_routers):
                router_name = input("Masukkan nama router: ")
                new_router = Router(router_name)
                num_routes = int(input(f"Masukkan jumlah rute untuk router {router_name}: "))
                for _ in range(num_routes):
                    dest = input("Masukkan tujuan: ")
                    next_hop = input("Masukkan next hop: ")
                    new_router.add_route(dest, next_hop)
                new_area.add_router(new_router)
            network.add_area(new_area)
            print(f"Region {region_name} ditambahkan.")
            network.visualize_network()
        elif choice == '4':
            region_name = input("Masukkan nama region yang akan dihapus: ")
            network.remove_area(region_name)
            print(f"Region {region_name} dihapus.")
            network.visualize_network()
        elif choice == '5':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    menu()
