from scapy.all import rdpcap, IP, UDP
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter(tags=["rip"])

current_dir = os.path.dirname(os.path.abspath(__file__))
pcap_file = os.path.join(current_dir, 'RIPv2_subnet_down.pcap')

pacotes = rdpcap(pcap_file)

app = FastAPI()

nodes = set()
edges = set()

for packet in pacotes:
    if IP in packet and UDP in packet:
        if packet[UDP].dport == 520 or packet[UDP].dport == 521:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            nodes.add(src_ip)
            nodes.add(dst_ip)
            edges.add((src_ip, dst_ip))

@router.get("/", response_class=HTMLResponse)
async def get_rip_graph():
    content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RIP Grafo</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style>
            #network {{
                width: 100%;
                height: 100vh;
                border: 1px solid lightgray;
            }}
        </style>
    </head>
    <body>
        <div id="network"></div>
        <script type="text/javascript">
            var nodes = new vis.DataSet([
                {', '.join(f"{{id: '{node}', label: '{node}'}}" for node in nodes)}
            ]);
            var edges = new vis.DataSet([
                {', '.join(f"{{from: '{src}', to: '{dst}'}}" for src, dst in edges)}
            ]);

            var container = document.getElementById('network');
            var data = {{
                nodes: nodes,
                edges: edges
            }};
            var options = {{
                physics: {{
                    stabilization: false,
                    barnesHut: {{
                        springLength: 200
                    }}
                }},
                layout: {{
                    hierarchical: {{
                        direction: 'UD',
                        sortMethod: 'directed'
                    }}
                }}
            }};
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """
    return content

app.include_router(router)