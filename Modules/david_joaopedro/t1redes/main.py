from scapy.all import rdpcap, IP
from collections import Counter
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()
router = APIRouter(tags=["ipv4"])

current_dir = os.path.dirname(os.path.abspath(__file__))
pcap_file = os.path.join(current_dir, 'trabalho1.pcap')

pacotes = rdpcap(pcap_file)

protocols = [packet[IP].proto for packet in pacotes if IP in packet]

contador = Counter(protocols)

nomes = {
    2: "IGMPv2",
    6: "TCP",
    17: "UDP"
}

titulos = [nomes.get(proto, f"Protocol {proto}") for proto in contador.keys()]
valores = list(contador.values())

cores = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)']

@router.get("/", response_class=HTMLResponse)
async def get_protocols():
    content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uso de Protocolos</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <div style="width:1920px;height:1080px;">
            <canvas id="myChart"></canvas>
        </div>
        <script>
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(titulos)},
                datasets: [{{
                    label: 'Uso de Protocolos',
                    data: {json.dumps(valores)},
                    backgroundColor: {json.dumps(cores)},
                    borderColor: 'rgba(0, 0, 0, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        </script>
    </body>
    </html>
    """
    return content

app.include_router(router)