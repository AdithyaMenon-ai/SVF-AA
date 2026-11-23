from pathlib import Path
from dataclasses import asdict
from datetime import datetime, timezone
import json
import uuid
from svf_aa.core.schemas import FrameworkResult


class VerificationLogger:
    def __init__(self, directory="outputs/verification_logs"):
        self.directory = Path(directory)

    def log(self, result: FrameworkResult) -> str:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / f"{uuid.uuid4().hex}.json"
        payload = asdict(result)
        payload["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return str(path)
