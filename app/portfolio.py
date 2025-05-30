import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self):
        self.file_path = 'app/resources/skills.csv'
        self.data = pd.read_csv(self.file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name='Portfolio')
    
    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                primary_link = str(row['Link1']) if pd.notna(row['Link1']) else ''
                secondary_link = str(row['Link2']) if pd.notna(row['Link2']) else ''
                tech_stack = str(row['TechStack']) if pd.notna(row['TechStack']) else ''
                self.collection.add(
                    documents=[tech_stack],
                    metadatas={
                        'primary_links': primary_link,
                        'secondary_links': secondary_link
                    },
                    ids=[str(uuid.uuid4())]
                )
    
    def query_links(self, skills):
        links = self.collection.query(
            query_texts=skills,
            n_results=1
        ).get('metadatas', [])
        return links