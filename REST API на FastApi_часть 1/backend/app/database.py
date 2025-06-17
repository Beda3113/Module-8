from typing import Dict
from .models import Advertisement

# Хранилище объявлений в памяти
advertisements_db: Dict[int, Advertisement] = {}
current_id: int = 1