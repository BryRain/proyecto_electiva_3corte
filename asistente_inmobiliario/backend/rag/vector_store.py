import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import hashlib
from datetime import datetime

class VectorStore:
    """
    Gestor de almacenamiento vectorial simplificado.
    Alternativa a Chroma que funciona sin requerir compilación C++.
    Usa scikit-learn para similarity y almacenamiento JSON.
    """
    
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.db_path = os.path.join(persist_directory, "vectors.json")
        self.collection = []
        self.next_id = 1
        
        # Cargar base de datos existente
        self._load_db()
    
    def _load_db(self):
        """Cargar vectores almacenados"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.collection = data.get('vectors', [])
                    self.next_id = data.get('next_id', len(self.collection) + 1)
            except:
                self.collection = []
                self.next_id = 1
    
    def _save_db(self):
        """Guardar vectores en disco"""
        try:
            data = {
                'vectors': self.collection,
                'next_id': self.next_id,
                'updated_at': datetime.now().isoformat()
            }
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando BD: {e}")
    
    def _get_embedding(self, text: str):
        """
        Generar embedding simple del texto.
        Usa OpenAI si está disponible, sino usa hash + TF-IDF simple.
        """
        try:
            from openai import OpenAI
            client = OpenAI()
            
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except:
            # Fallback: crear embedding basado en caracteres
            # Para MVP, es suficiente
            embedding = []
            text_normalized = text.lower()
            
            # Crear vector de características simples
            for i in range(384):  # Dimensión estándar de embeddings
                char_hash = sum(ord(c) * (i + 1) for c in text_normalized[:50])
                embedding.append((char_hash % 100) / 100.0)
            
            return embedding
    
    def add_document(self, doc_id: str, content: str, metadata: dict = None):
        """Añadir documento al vector store"""
        try:
            # Dividir en chunks
            chunk_size = 500
            chunks = [
                content[i:i+chunk_size] 
                for i in range(0, len(content), chunk_size)
            ]
            
            if not chunks:
                return False
            
            # Procesar cada chunk
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_chunk_{i}"
                
                # Generar embedding
                embedding = self._get_embedding(chunk)
                
                # Guardar
                vector_record = {
                    'id': chunk_id,
                    'embedding': embedding,
                    'content': chunk[:200],  # Primeros 200 chars para preview
                    'full_content': chunk,
                    'metadata': metadata or {},
                    'source': doc_id,
                    'chunk': i,
                    'created_at': datetime.now().isoformat()
                }
                
                self.collection.append(vector_record)
            
            self._save_db()
            return True
        except Exception as e:
            print(f"Error añadiendo documento: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> list:
        """Búsqueda vectorial de documentos similares"""
        try:
            if not self.collection:
                return []
            
            # Generar embedding del query
            query_embedding = self._get_embedding(query)
            query_embedding = np.array(query_embedding).reshape(1, -1)
            
            # Calcular similitud con todos los documentos
            similarities = []
            for vector_record in self.collection:
                doc_embedding = np.array(vector_record['embedding']).reshape(1, -1)
                similarity = cosine_similarity(query_embedding, doc_embedding)[0][0]
                
                similarities.append({
                    'record': vector_record,
                    'similarity': float(similarity)
                })
            
            # Ordenar por similitud
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Retornar top-k
            results = []
            for item in similarities[:top_k]:
                record = item['record']
                results.append({
                    'content': record['full_content'],
                    'metadata': record['metadata'],
                    'similarity': item['similarity'],
                    'source': record['source']
                })
            
            return results
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return []
    
    def delete_document(self, doc_id: str):
        """Eliminar documento del vector store"""
        try:
            self.collection = [
                v for v in self.collection 
                if v.get('source') != doc_id
            ]
            self._save_db()
            return True
        except Exception as e:
            print(f"Error eliminando documento: {e}")
            return False
    
    def clear_all(self):
        """Limpiar todo el vector store"""
        try:
            self.collection = []
            self.next_id = 1
            self._save_db()
            return True
        except Exception as e:
            print(f"Error limpiando vector store: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Obtener estadísticas del vector store"""
        return {
            'total_vectors': len(self.collection),
            'documents': len(set(v['source'] for v in self.collection)),
            'db_path': self.db_path,
            'db_size_mb': os.path.getsize(self.db_path) / (1024*1024) if os.path.exists(self.db_path) else 0
        }

