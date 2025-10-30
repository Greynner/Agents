"""
Utilidades para logging a Axiom
Módulo centralizado para envío de logs y métricas a Axiom
"""

import os
import requests
import json
import traceback
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class AxiomLogger:
    """Clase simplificada para enviar logs a Axiom"""
    
    def __init__(self):
        self.api_token = os.getenv('AXIOM_API_TOKEN')
        self.org_id = os.getenv('AXIOM_ORG_ID')
        self.dataset = os.getenv('AXIOM_DATASET', 'hannah-qa-agent')
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.ingest_url = f"https://api.axiom.co/v1/datasets/{self.dataset}/ingest"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}',
            'X-Axiom-Org-Id': self.org_id
        }
    
    def log(self, level: str, message: str, metadata: Optional[Dict] = None) -> bool:
        """Envía un log a Axiom"""
        if not self.api_token or not self.org_id:
            print(f"[{level}] {message}")
            return False
        
        try:
            log_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level.upper(),
                "message": message,
                "source": "hannah_qa_agent",
                "environment": self.environment,
                "metadata": metadata or {}
            }
            
            response = requests.post(
                self.ingest_url,
                headers=self.headers,
                json=[log_data],
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Log enviado: {message}")
                return True
            else:
                print(f"⚠️ Error enviando log: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error en logging: {str(e)}")
            return False
    
    def log_info(self, message: str, metadata: Optional[Dict] = None) -> bool:
        """Log de información"""
        return self.log("INFO", message, metadata)
    
    def log_error(self, message: str, error: Exception = None, context: Optional[Dict] = None) -> bool:
        """Log de error con detalles"""
        metadata = context or {}
        if error:
            metadata.update({
                "error_type": type(error).__name__,
                "error_message": str(error),
                "traceback": traceback.format_exc()
            })
        return self.log("ERROR", message, metadata)
    
    def log_warning(self, message: str, metadata: Optional[Dict] = None) -> bool:
        """Log de advertencia"""
        return self.log("WARN", message, metadata)


# Instancia global del logger
logger = AxiomLogger()


