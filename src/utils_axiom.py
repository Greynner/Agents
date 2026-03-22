"""
Utilidades para logging a Axiom
Módulo centralizado para envío de logs y métricas a Axiom
"""

import os
import requests
import traceback
from datetime import datetime, timezone
from typing import Dict, Optional


class AxiomLogger:
    """Clase para enviar logs a Axiom"""

    def __init__(self, source: str = "hannah_qa_agent"):
        self.source = source
        self.api_token = os.getenv("AXIOM_API_TOKEN")
        self.org_id = os.getenv("AXIOM_ORG_ID")
        self.dataset = os.getenv("AXIOM_DATASET", "hannah-qa-agent")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.ingest_url = f"https://api.axiom.co/v1/datasets/{self.dataset}/ingest"
        self.headers = (
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}",
                "X-Axiom-Org-Id": self.org_id,
            }
            if self.api_token and self.org_id
            else None
        )

    def log(self, level: str, message: str, metadata: Optional[Dict] = None) -> bool:
        if not self.headers:
            print(f"[{level}] {message}")
            return False

        try:
            log_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level.upper(),
                "message": message,
                "source": self.source,
                "environment": self.environment,
                "metadata": metadata or {},
            }
            response = requests.post(
                self.ingest_url,
                headers=self.headers,
                json=[log_data],
                timeout=5,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"[logging error] {e}")
            return False

    def log_info(self, message: str, metadata: Optional[Dict] = None) -> bool:
        return self.log("INFO", message, metadata)

    def log_error(
        self,
        message: str,
        error: Exception = None,
        context: Optional[Dict] = None,
    ) -> bool:
        metadata = context or {}
        if error:
            metadata.update(
                {
                    "error_type": type(error).__name__,
                    "error_message": str(error),
                    "traceback": traceback.format_exc(),
                }
            )
        return self.log("ERROR", message, metadata)

    def log_warning(self, message: str, metadata: Optional[Dict] = None) -> bool:
        return self.log("WARN", message, metadata)


# Instancia global del logger (para uso directo del módulo)
logger = AxiomLogger()
