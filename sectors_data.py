import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# 187 Sectors from PDF
SECTORS = [
    ("2/3 Wheelers", "Auto"), ("Abrasives & Bearings", "Industrial"),
    ("Advertising & Media Agencies", "Media"), ("Aerospace & Defense", "Defense"),
    ("Airline", "Transport"), ("Airport & Airport Services", "Transport"),
    ("Aluminium", "Metals"), ("Aluminium, Copper & Zinc Products", "Metals"),
    ("Amusement Parks / Recreation", "Leisure"), ("Animal Feed", "Agriculture"),
    ("Asset Management Company", "Finance"), ("Auto Components & Equipments", "Auto"),
    ("Auto Dealer", "Auto"), ("Biotechnology", "Healthcare"),
    ("Breweries & Distilleries", "FMCG"), ("BPO / KPO", "IT"),
    ("Cables - Electricals", "Electricals"), ("Carbon Black", "Chemicals"),
    ("Castings & Forgings", "Industrial"), ("Cement & Cement Products", "Construction"),
    ("Ceramics", "Construction"), ("Cigarettes & Tobacco Products", "FMCG"),
    ("Civil Construction", "Construction"), ("Coal", "Energy"),
    ("Commercial Vehicles", "Auto"), ("Commodity Chemicals", "Chemicals"),
    ("Compressors, Pumps & Engines", "Industrial"), ("Computers - Software & Consulting", "IT"),
    ("Computers Hardware & Equipments", "IT"), ("Construction Vehicles", "Auto"),
    ("Consulting Services", "Services"), ("Consumer Electronics", "Electronics"),
    ("Copper", "Metals"), ("Dairy Products", "FMCG"),
    ("Data Processing Services", "IT"), ("Dealers - Vehicles", "Auto"),
    ("Depositories, Clearing Houses", "Finance"), ("Digital Entertainment", "Media"),
    ("Distributors", "Services"), ("Diversified", "Diversified"),
    ("Diversified Commercial Services", "Services"), ("Diversified Consumer Products", "FMCG"),
    ("Diversified FMCG", "FMCG"), ("Diversified Metals", "Metals"),
    ("Diversified Retail", "Retail"), ("Dredging", "Construction"),
    ("Dyes & Pigments", "Chemicals"), ("E-Learning", "Education"),
    ("E-Commerce", "Retail"), ("Edible Oil", "FMCG"),
    ("Education", "Education"), ("Electrodes & Refractories", "Industrial"),
    ("Electronic Media", "Media"), ("Exchange & Data Platform", "Finance"),
    ("Explosives", "Chemicals"), ("Ferro & Silica Manganese", "Metals"),
    ("Fertilizers", "Agriculture"), ("Film Production & Distribution", "Media"),
    ("Financial Institution", "Finance"), ("Financial Products Distributor", "Finance"),
    ("Financial Technology (Fintech)", "Finance"), ("Footwear", "Consumer"),
    ("Forest Products", "Agriculture"), ("Furniture & Home Furnishing", "Consumer"),
    ("Garments & Apparels", "Textile"), ("Gas Transmission / Marketing", "Energy"),
    ("Gems, Jewellery & Watches", "Consumer"), ("General Insurance", "Insurance"),
    ("Glass - Consumer", "Consumer"), ("Glass - Industrial", "Industrial"),
    ("Granites & Marbles", "Construction"), ("Healthcare Research & Analytics", "Healthcare"),
    ("Healthcare Service Provider", "Healthcare"), ("Heavy Electrical Equipment", "Electricals"),
    ("Holding Company", "Finance"), ("Hospital", "Healthcare"),
    ("Hotels & Resorts", "Hospitality"), ("Household Appliances", "Consumer"),
    ("Household Products", "FMCG"), ("Houseware", "Consumer"),
    ("Housing Finance Company", "Finance"), ("Industrial Gases", "Chemicals"),
    ("Industrial Minerals", "Mining"), ("Industrial Products", "Industrial"),
    ("Insurance Distributors", "Insurance"), ("Integrated Power Utilities", "Energy"),
    ("Internet & Catalogue Retail", "Retail"), ("Investment Company", "Finance"),
    ("Iron & Steel", "Metals"), ("Iron & Steel Products", "Metals"),
    ("IT Enabled Services", "IT"), ("Jute & Jute Products", "Textile"),
    ("Leather & Leather Products", "Consumer"), ("Leisure Products", "Leisure"),
    ("Life Insurance", "Insurance"), ("Logistics Solution Provider", "Logistics"),
    ("LPG / CNG / LNG Supplier", "Energy"), ("Lubricants", "Energy"),
    ("Meat Products / Poultry", "FMCG"), ("Media & Entertainment", "Media"),
    ("Medical Equipment & Supplies", "Healthcare"), ("Microfinance Institutions", "Finance"),
    ("Multi Utilities", "Energy"), ("NBFC", "Finance"),
    ("Offshore Drilling Services", "Energy"), ("Oil Equipment & Services", "Energy"),
    ("Oil Exploration & Production", "Energy"), ("Oil Storage & Transportation", "Energy"),
    ("Other Agricultural Products", "Agriculture"), ("Other Bank", "Finance"),
    ("Other Beverages", "FMCG"), ("Other Capital Market Services", "Finance"),
    ("Other Construction Materials", "Construction"), ("Other Consumer Services", "Services"),
    ("Other Electrical Equipment", "Electricals"), ("Other Financial Services", "Finance"),
    ("Other Food Products", "FMCG"), ("Other Industrial Products", "Industrial"),
    ("Other Telecom Services", "Telecom"), ("Other Textile Products", "Textile"),
    ("Packaged Foods", "FMCG"), ("Packaging", "Industrial"),
    ("Paints", "Chemicals"), ("Paper & Paper Products", "Industrial"),
    ("Passenger Cars & Utility Vehicles", "Auto"), ("Personal Care", "FMCG"),
    ("Pesticides & Agrochemicals", "Agriculture"), ("Petrochemicals", "Chemicals"),
    ("Pharmaceuticals", "Healthcare"), ("Pharmacy Retail", "Healthcare"),
    ("Pig Iron", "Metals"), ("Plastic Products - Consumer", "Consumer"),
    ("Plastic Products - Industrial", "Industrial"), ("Plywood & Laminates", "Construction"),
    ("Port & Port Services", "Logistics"), ("Power Transmission", "Energy"),
    ("Power Distribution", "Energy"), ("Power Generation", "Energy"),
    ("Power Trading", "Energy"), ("Precious Metals", "Metals"),
    ("Print Media", "Media"), ("Printing & Publication", "Media"),
    ("Printing Inks", "Chemicals"), ("Private Sector Bank", "Finance"),
    ("Public Sector Bank", "Finance"), ("Railway Wagons", "Industrial"),
    ("Ratings", "Finance"), ("REITs", "Finance"),
    ("Real Estate Services", "Real Estate"), ("Refineries & Marketing", "Energy"),
    ("Residential & Commercial Projects", "Real Estate"), ("Restaurants", "Hospitality"),
    ("Road Assets", "Infrastructure"), ("Road Transport", "Transport"),
    ("Rubber", "Industrial"), ("Sanitary Ware", "Construction"),
    ("Seafood", "FMCG"), ("Ship Building", "Industrial"),
    ("Shipping", "Logistics"), ("Software Products", "IT"),
    ("Speciality Retail", "Retail"), ("Specialty Chemicals", "Chemicals"),
    ("Sponge Iron", "Metals"), ("Stationery", "Consumer"),
    ("Stockbroking & Allied", "Finance"), ("Sugar", "FMCG"),
    ("Tea & Coffee", "FMCG"), ("Telecom Equipment", "Telecom"),
    ("Telecom Services", "Telecom"), ("Telecom Infrastructure", "Telecom"),
    ("Travel Services", "Hospitality"), ("Tractors", "Auto"),
    ("Trading - Auto Components", "Trading"), ("Trading - Chemicals", "Trading"),
    ("Trading - Gas", "Trading"), ("Trading - Metals", "Trading"),
    ("Trading - Minerals", "Trading"), ("Trading - Textile", "Trading"),
    ("Trading & Distributors", "Trading"), ("Transport Services", "Transport"),
    ("TV Broadcasting", "Media"), ("Tyres & Rubber Products", "Industrial"),
    ("Waste Management", "Services"), ("Water Supply & Management", "Services"),
    ("Web-based Media", "Media"), ("Wellness", "Healthcare"), ("Zinc", "Metals"),
]

def insert_sectors():
    print("📥 Inserting 187 sectors...\n")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    inserted = 0
    for sector_name, industry_name in SECTORS:
        cursor.execute("""
            INSERT INTO sectors (sector_name, industry_name)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (sector_name, industry_name))
        inserted += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ {inserted} sectors inserted successfully!")

if __name__ == "__main__":
    insert_sectors()