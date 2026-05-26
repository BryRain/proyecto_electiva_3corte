from PyPDF2 import PdfReader
import hashlib
import os
from backend.database.models import db, Document

class DocumentProcessor:
    """Procesar documentos (PDFs) para el sistema RAG"""
    
    @staticmethod
    def extract_pdf_content(pdf_path: str) -> str:
        """Extraer texto de PDF"""
        try:
            content = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    content += page.extract_text()
            return content
        except Exception as e:
            print(f"Error extrayendo PDF: {e}")
            return ""
    
    @staticmethod
    def calculate_hash(content: str) -> str:
        """Calcular hash SHA256 del contenido"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    @staticmethod
    def process_document(file_path: str, vector_store) -> bool:
        """Procesar documento y añadirlo al vector store"""
        try:
            filename = os.path.basename(file_path)
            
            # Extraer contenido
            if file_path.endswith('.pdf'):
                content = DocumentProcessor.extract_pdf_content(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            if not content:
                return False
            
            # Calcular hash
            content_hash = DocumentProcessor.calculate_hash(content)
            
            # Verificar si ya existe
            existing_doc = Document.query.filter_by(content_hash=content_hash).first()
            if existing_doc:
                return False
            
            # Crear registro en BD
            doc = Document(
                filename=filename,
                content=content,
                content_hash=content_hash,
                processed=False
            )
            db.session.add(doc)
            db.session.flush()  # Para obtener el ID
            
            # Añadir al vector store
            if vector_store.add_document(
                doc_id=f"doc_{doc.id}",
                content=content,
                metadata={'filename': filename, 'doc_id': doc.id}
            ):
                doc.processed = True
                # Contar chunks (aproximado)
                doc.chunks_count = len(content) // 500
                db.session.commit()
                return True
            else:
                db.session.rollback()
                return False
        
        except Exception as e:
            print(f"Error procesando documento: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def process_documents_from_directory(documents_dir: str, vector_store) -> dict:
        """Procesar todos los documentos en un directorio"""
        stats = {'total': 0, 'processed': 0, 'failed': 0}
        
        if not os.path.exists(documents_dir):
            os.makedirs(documents_dir)
            return stats
        
        for filename in os.listdir(documents_dir):
            if filename.endswith(('.pdf', '.txt')):
                file_path = os.path.join(documents_dir, filename)
                stats['total'] += 1
                
                if DocumentProcessor.process_document(file_path, vector_store):
                    stats['processed'] += 1
                else:
                    stats['failed'] += 1
        
        return stats
