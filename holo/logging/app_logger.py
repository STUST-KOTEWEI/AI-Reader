"""
Logging System Module

Provides structured logging for the application.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import logging
import json
import os


class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """
    Represents a log entry.
    
    Attributes:
        timestamp: When the log was created
        level: Log level
        message: Log message
        logger_name: Name of the logger
        module: Module name
        function: Function name
        line: Line number
        extra: Additional log data
    """
    timestamp: str
    level: str
    message: str
    logger_name: str = ""
    module: str = ""
    function: str = ""
    line: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created).isoformat(),
            level=record.levelname,
            message=record.getMessage(),
            logger_name=record.name,
            module=record.module,
            function=record.funcName,
            line=record.lineno,
            extra=getattr(record, 'extra', {})
        )
        return log_entry.to_json()


class ColorFormatter(logging.Formatter):
    """Colored console formatter."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[41m',  # Red background
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


class AppLogger:
    """Application logger with structured logging support."""
    
    def __init__(
        self,
        name: str = "ai_reader",
        log_dir: str = "logs",
        log_level: str = "INFO",
        enable_console: bool = True,
        enable_file: bool = True,
        enable_json: bool = True
    ):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent duplicate handlers
        self.logger.handlers = []
        
        if enable_console:
            self._add_console_handler()
        
        if enable_file:
            self._add_file_handler()
        
        if enable_json:
            self._add_json_handler()
    
    def _ensure_log_dir(self):
        """Ensure log directory exists."""
        os.makedirs(self.log_dir, exist_ok=True)
    
    def _add_console_handler(self):
        """Add colored console handler."""
        handler = logging.StreamHandler()
        handler.setFormatter(ColorFormatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        ))
        self.logger.addHandler(handler)
    
    def _add_file_handler(self):
        """Add file handler for text logs."""
        self._ensure_log_dir()
        handler = logging.FileHandler(
            os.path.join(self.log_dir, f"{self.name}.log"),
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s'
        ))
        self.logger.addHandler(handler)
    
    def _add_json_handler(self):
        """Add JSON file handler for structured logs."""
        self._ensure_log_dir()
        handler = logging.FileHandler(
            os.path.join(self.log_dir, f"{self.name}.json.log"),
            encoding='utf-8'
        )
        handler.setFormatter(JSONFormatter())
        self.logger.addHandler(handler)
    
    def debug(self, message: str, **extra):
        """Log debug message."""
        self.logger.debug(message, extra={'extra': extra})
    
    def info(self, message: str, **extra):
        """Log info message."""
        self.logger.info(message, extra={'extra': extra})
    
    def warning(self, message: str, **extra):
        """Log warning message."""
        self.logger.warning(message, extra={'extra': extra})
    
    def error(self, message: str, **extra):
        """Log error message."""
        self.logger.error(message, extra={'extra': extra})
    
    def critical(self, message: str, **extra):
        """Log critical message."""
        self.logger.critical(message, extra={'extra': extra})
    
    def exception(self, message: str, **extra):
        """Log exception with traceback."""
        self.logger.exception(message, extra={'extra': extra})


class PerformanceMonitor:
    """Monitors performance metrics."""
    
    def __init__(self, logger: Optional[AppLogger] = None):
        self.logger = logger or get_app_logger()
        self._metrics: Dict[str, List[float]] = {}
        self._counters: Dict[str, int] = {}
    
    def record_timing(self, operation: str, duration_ms: float):
        """Record a timing metric."""
        if operation not in self._metrics:
            self._metrics[operation] = []
        self._metrics[operation].append(duration_ms)
        
        self.logger.debug(
            f"Performance: {operation}",
            operation=operation,
            duration_ms=duration_ms
        )
    
    def increment_counter(self, name: str, value: int = 1):
        """Increment a counter."""
        if name not in self._counters:
            self._counters[name] = 0
        self._counters[name] += value
    
    def get_metrics(self, operation: str) -> Dict[str, float]:
        """Get metrics for an operation."""
        timings = self._metrics.get(operation, [])
        if not timings:
            return {}
        
        return {
            "count": len(timings),
            "min_ms": min(timings),
            "max_ms": max(timings),
            "avg_ms": sum(timings) / len(timings),
            "total_ms": sum(timings)
        }
    
    def get_counter(self, name: str) -> int:
        """Get counter value."""
        return self._counters.get(name, 0)
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        return {
            "timings": {
                op: self.get_metrics(op) 
                for op in self._metrics
            },
            "counters": self._counters.copy()
        }
    
    def reset(self):
        """Reset all metrics."""
        self._metrics = {}
        self._counters = {}


class RequestLogger:
    """Logs HTTP requests and responses."""
    
    def __init__(self, logger: Optional[AppLogger] = None):
        self.logger = logger or get_app_logger()
    
    def log_request(
        self,
        method: str,
        path: str,
        client_ip: str = "",
        user_id: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """Log an incoming request."""
        self.logger.info(
            f"Request: {method} {path}",
            method=method,
            path=path,
            client_ip=client_ip,
            user_id=user_id,
            headers=headers or {}
        )
    
    def log_response(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        response_size: int = 0
    ):
        """Log a response."""
        level = "info" if status_code < 400 else "error"
        getattr(self.logger, level)(
            f"Response: {method} {path} {status_code} ({duration_ms:.2f}ms)",
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=duration_ms,
            response_size=response_size
        )


class AuditLogger:
    """Logs security and audit events."""
    
    def __init__(self, logger: Optional[AppLogger] = None):
        self.logger = logger or AppLogger(name="audit", log_level="INFO")
    
    def log_login(self, user_id: str, success: bool, ip_address: str = ""):
        """Log a login attempt."""
        status = "successful" if success else "failed"
        self.logger.info(
            f"Login {status}: {user_id}",
            event="login",
            user_id=user_id,
            success=success,
            ip_address=ip_address
        )
    
    def log_logout(self, user_id: str):
        """Log a logout."""
        self.logger.info(
            f"Logout: {user_id}",
            event="logout",
            user_id=user_id
        )
    
    def log_access(
        self,
        user_id: str,
        resource: str,
        action: str,
        allowed: bool
    ):
        """Log resource access."""
        status = "allowed" if allowed else "denied"
        level = "info" if allowed else "warning"
        getattr(self.logger, level)(
            f"Access {status}: {user_id} -> {action} on {resource}",
            event="access",
            user_id=user_id,
            resource=resource,
            action=action,
            allowed=allowed
        )
    
    def log_data_change(
        self,
        user_id: str,
        entity: str,
        entity_id: str,
        action: str,
        old_value: Optional[Dict] = None,
        new_value: Optional[Dict] = None
    ):
        """Log a data change."""
        self.logger.info(
            f"Data change: {user_id} {action} {entity}/{entity_id}",
            event="data_change",
            user_id=user_id,
            entity=entity,
            entity_id=entity_id,
            action=action,
            old_value=old_value,
            new_value=new_value
        )


# Global instances
_app_logger: Optional[AppLogger] = None
_performance_monitor: Optional[PerformanceMonitor] = None
_request_logger: Optional[RequestLogger] = None
_audit_logger: Optional[AuditLogger] = None


def get_app_logger() -> AppLogger:
    """Get the global app logger instance."""
    global _app_logger
    if _app_logger is None:
        _app_logger = AppLogger()
    return _app_logger


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def get_request_logger() -> RequestLogger:
    """Get the global request logger instance."""
    global _request_logger
    if _request_logger is None:
        _request_logger = RequestLogger()
    return _request_logger


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger
