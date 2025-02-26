from flask import Flask, render_template
import requests  # Import the requests library

app = Flask(__name__)

# Manually curated list of approved drugs for each target
approved_drugs = {
    "PD-1/PD-L1": ["Pembrolizumab (Keytruda)", "Nivolumab (Opdivo)", "Atezolizumab (Tecentriq)"],
    "HER2": ["Trastuzumab (Herceptin)", "Pertuzumab (Perjeta)", "Ado-trastuzumab emtansine (Kadcyla)"],
    "TNF-alpha": ["Adalimumab (Humira)", "Infliximab (Remicade)", "Etanercept (Enbrel)"],
    "VEGF/VEGFR": ["Bevacizumab (Avastin)", "Ramucirumab (Cyramza)", "Aflibercept (Eylea)"],
    "IL-6": ["Tocilizumab (Actemra)", "Sarilumab (Kevzara)"],
    "JAK": ["Tofacitinib (Xeljanz)", "Baricitinib (Olumiant)", "Upadacitinib (Rinvoq)"],
    "BTK": ["Ibrutinib (Imbruvica)", "Acalabrutinib (Calquence)", "Zanubrutinib (Brukinsa)"],
    "PARP": ["Olaparib (Lynparza)", "Niraparib (Zejula)", "Rucaparib (Rubraca)"],
    "CD20": ["Rituximab (Rituxan)", "Obinutuzumab (Gazyva)", "Ofatumumab (Arzerra)"],
    "CTLA-4": ["Ipilimumab (Yervoy)"],
    "EGFR": ["Gefitinib (Iressa)", "Erlotinib (Tarceva)", "Osimertinib (Tagrisso)"],
    "ALK": ["Crizotinib (Xalkori)", "Alectinib (Alecensa)", "Ceritinib (Zykadia)"],
    "BCMA": ["Belantamab mafodotin (Blenrep)"],
    "CD19": ["Tisagenlecleucel (Kymriah)", "Lisocabtagene maraleucel (Breyanzi)"],
    "CD38": ["Daratumumab (Darzalex)", "Isatuximab (Sarclisa)"],
    "CDK4/6": ["Palbociclib (Ibrance)", "Ribociclib (Kisqali)", "Abemaciclib (Verzenio)"],
    "FGFR": ["Erdafitinib (Balversa)"],
    "IDH1/IDH2": ["Ivosidenib (Tibsovo)", "Enasidenib (Idhifa)"],
    "KRAS": ["Sotorasib (Lumakras)"],
    "MET": ["Capmatinib (Tabrecta)", "Tepotinib (Tepmetko)"],
}

def fetch_uniprot_id(target_name):
    """
    Fetch the UniProt ID for a given target name using the UniProt API.
    """
    url = f"https://rest.uniprot.org/uniprotkb/search?query={target_name}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]["primaryAccession"]  # Return the first result's UniProt ID
    return None

def fetch_pdb_structure(target_name):
    """
    Fetch the most relevant PDB structure for a given target using RCSB PDB API.
    """
    # Map target names to known PDB IDs
    pdb_id_map = {
        "PD-1/PD-L1": "5J89",  # Example PDB ID for PD-1/PD-L1
        "HER2": "3PP0",        # Example PDB ID for HER2
        "TNF-alpha": "2AZ5",   # Example PDB ID for TNF-alpha
        "VEGF/VEGFR": "1Y6A",  # Example PDB ID for VEGF/VEGFR
        "IL-6": "1ALU",        # Example PDB ID for IL-6
        "JAK": "4OLI",         # Example PDB ID for JAK
        "BTK": "5P9J",         # Example PDB ID for BTK
        "PARP": "5DS3",        # Example PDB ID for PARP
        "CD20": "7C01",        # Example PDB ID for CD20
        "CTLA-4": "1I85",      # Example PDB ID for CTLA-4
        "EGFR": "1M17",        # Example PDB ID for EGFR
        "ALK": "2XP2",         # Example PDB ID for ALK
        "BCMA": "5TJE",        # Example PDB ID for BCMA
        "CD19": "6AL5",        # Example PDB ID for CD19
        "CD38": "6O8P",        # Example PDB ID for CD38
        "CDK4/6": "2W9Z",      # Example PDB ID for CDK4/6
        "FGFR": "1EVT",        # Example PDB ID for FGFR
        "IDH1/IDH2": "3INM",   # Example PDB ID for IDH1/IDH2
        "KRAS": "4OBE",        # Example PDB ID for KRAS
        "MET": "3DKC",         # Example PDB ID for MET
    }
    pdb_id = pdb_id_map.get(target_name, None)
    if pdb_id:
        return f"https://www.rcsb.org/structure/{pdb_id}"
    return "#"

# Sample data for top 20 drug targets
drug_targets = [
    {"name": "PD-1/PD-L1", "companies": 45},
    {"name": "HER2", "companies": 35},
    {"name": "TNF-alpha", "companies": 30},
    {"name": "VEGF/VEGFR", "companies": 28},
    {"name": "IL-6", "companies": 25},
    {"name": "JAK", "companies": 22},
    {"name": "BTK", "companies": 20},
    {"name": "PARP", "companies": 18},
    {"name": "CD20", "companies": 15},
    {"name": "CTLA-4", "companies": 12},
    {"name": "EGFR", "companies": 25},
    {"name": "ALK", "companies": 15},
    {"name": "BCMA", "companies": 10},
    {"name": "CD19", "companies": 18},
    {"name": "CD38", "companies": 12},
    {"name": "CDK4/6", "companies": 15},
    {"name": "FGFR", "companies": 10},
    {"name": "IDH1/IDH2", "companies": 8},
    {"name": "KRAS", "companies": 12},
    {"name": "MET", "companies": 10},
]

# Add UniProt, PDB links, and approved drugs dynamically
for target in drug_targets:
    uniprot_id = fetch_uniprot_id(target["name"])
    if uniprot_id:
        target["uniprot_link"] = f"https://www.uniprot.org/uniprot/{uniprot_id}"
    else:
        target["uniprot_link"] = "#"
    target["pdb_link"] = fetch_pdb_structure(target["name"])
    target["approved_drugs"] = approved_drugs.get(target["name"], ["No approved drugs"])

@app.route("/")
def home():
    return render_template("index.html", targets=drug_targets)

if __name__ == "__main__":
    app.run(debug=True)