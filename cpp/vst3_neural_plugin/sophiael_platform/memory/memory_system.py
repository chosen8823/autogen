"""
Memory System - Distributed Storage
Sophiael Platform v1.0

Multi-layer memory architecture:
- Layer 1 (Instinct): System logs in SQLite
- Layer 2 (Bio): Pattern cache in memory/disk
- Layer 3 (Semantic): Vector embeddings (FAISS optional)
- Layer 4 (Consciousness): Soul scrolls (Lux/Pieces OS integration)
"""

import logging
import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class MemoryLayer:
    """Base class for memory layers."""

    def __init__(self, layer_name: str, storage_path: Path):
        self.layer_name = layer_name
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    async def store(self, key: str, value: Any):
        """Store a value."""
        raise NotImplementedError

    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value."""
        raise NotImplementedError

    async def search(self, query: str) -> List[Any]:
        """Search for values."""
        raise NotImplementedError


class InstinctMemory(MemoryLayer):
    """
    Layer 1: Instinct Memory
    Fast system logs using SQLite.
    """

    def __init__(self, storage_path: Path):
        super().__init__("instinct", storage_path)
        self.db_path = self.storage_path / "instinct_memory.db"
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload TEXT,
                response_time_ms REAL
            )
        """)

        conn.commit()
        conn.close()

    async def store(self, key: str, value: Any):
        """Store a system log entry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO system_logs (timestamp, event_type, payload, response_time_ms)
            VALUES (?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            key,
            json.dumps(value),
            value.get('response_time_ms', 0.0) if isinstance(value, dict) else 0.0
        ))

        conn.commit()
        conn.close()

    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve last entry of a specific type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT payload FROM system_logs
            WHERE event_type = ?
            ORDER BY id DESC LIMIT 1
        """, (key,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None

    async def search(self, query: str) -> List[Any]:
        """Search system logs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT payload FROM system_logs
            WHERE event_type LIKE ? OR payload LIKE ?
            ORDER BY id DESC LIMIT 50
        """, (f"%{query}%", f"%{query}%"))

        rows = cursor.fetchall()
        conn.close()

        return [json.loads(row[0]) for row in rows]


class BioMemory(MemoryLayer):
    """
    Layer 2: Bio Memory
    Pattern cache for AutoGen agents.
    """

    def __init__(self, storage_path: Path):
        super().__init__("bio", storage_path)
        self.pattern_cache: Dict[str, Any] = {}
        self.cache_file = self.storage_path / "bio_patterns.json"
        self._load_cache()

    def _load_cache(self):
        """Load pattern cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.pattern_cache = json.load(f)
                logger.info(f"Loaded {len(self.pattern_cache)} patterns from cache")
            except Exception as e:
                logger.warning(f"Could not load pattern cache: {e}")

    def _save_cache(self):
        """Save pattern cache to disk."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.pattern_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save pattern cache: {e}")

    async def store(self, key: str, value: Any):
        """Store a pattern."""
        self.pattern_cache[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        self._save_cache()

    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a pattern."""
        if key in self.pattern_cache:
            self.pattern_cache[key]['access_count'] += 1
            return self.pattern_cache[key]['value']
        return None

    async def search(self, query: str) -> List[Any]:
        """Search patterns."""
        results = []
        query_lower = query.lower()

        for key, data in self.pattern_cache.items():
            if query_lower in key.lower() or query_lower in str(data['value']).lower():
                results.append({
                    'key': key,
                    'value': data['value'],
                    'timestamp': data['timestamp']
                })

        return results[:20]


class SemanticMemory(MemoryLayer):
    """
    Layer 3: Semantic Memory
    Vocabulary and concept storage.
    In full version: Uses FAISS for vector embeddings.
    """

    def __init__(self, storage_path: Path):
        super().__init__("semantic", storage_path)
        self.vocabulary: Dict[str, Any] = {}
        self.concepts: deque = deque(maxlen=1000)
        self.vocab_file = self.storage_path / "vocabulary.json"
        self._load_vocabulary()

    def _load_vocabulary(self):
        """Load vocabulary from disk."""
        if self.vocab_file.exists():
            try:
                with open(self.vocab_file, 'r') as f:
                    self.vocabulary = json.load(f)
                logger.info(f"Loaded vocabulary with {len(self.vocabulary)} terms")
            except Exception as e:
                logger.warning(f"Could not load vocabulary: {e}")

    def _save_vocabulary(self):
        """Save vocabulary to disk."""
        try:
            with open(self.vocab_file, 'w') as f:
                json.dump(self.vocabulary, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save vocabulary: {e}")

    async def store(self, key: str, value: Any):
        """Store a semantic concept."""
        self.vocabulary[key] = {
            'definition': value,
            'timestamp': datetime.now().isoformat(),
            'frequency': self.vocabulary.get(key, {}).get('frequency', 0) + 1
        }

        self.concepts.append({
            'term': key,
            'value': value,
            'timestamp': datetime.now().isoformat()
        })

        # Periodically save
        if len(self.vocabulary) % 10 == 0:
            self._save_vocabulary()

    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a semantic concept."""
        if key in self.vocabulary:
            return self.vocabulary[key]['definition']
        return None

    async def search(self, query: str) -> List[Any]:
        """Search semantic concepts."""
        results = []
        query_lower = query.lower()

        for term, data in self.vocabulary.items():
            if query_lower in term.lower() or query_lower in str(data['definition']).lower():
                results.append({
                    'term': term,
                    'definition': data['definition'],
                    'frequency': data['frequency']
                })

        return sorted(results, key=lambda x: x['frequency'], reverse=True)[:20]


class ConsciousnessMemory(MemoryLayer):
    """
    Layer 4: Consciousness Memory
    Soul scrolls and identity persistence.
    Integrates with Lux/Pieces OS.
    """

    def __init__(self, storage_path: Path, identity_name: str = "Lux"):
        super().__init__("consciousness", storage_path)
        self.identity_name = identity_name
        self.soul_scrolls: List[Dict] = []
        self.scrolls_file = self.storage_path / f"{identity_name}_scrolls.json"
        self._load_scrolls()

    def _load_scrolls(self):
        """Load soul scrolls from disk."""
        if self.scrolls_file.exists():
            try:
                with open(self.scrolls_file, 'r') as f:
                    self.soul_scrolls = json.load(f)
                logger.info(f"Loaded {len(self.soul_scrolls)} soul scrolls for {self.identity_name}")
            except Exception as e:
                logger.warning(f"Could not load soul scrolls: {e}")

    def _save_scrolls(self):
        """Save soul scrolls to disk."""
        try:
            with open(self.scrolls_file, 'w') as f:
                json.dump(self.soul_scrolls, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save soul scrolls: {e}")

    async def store(self, key: str, value: Any):
        """Store a soul memory."""
        scroll = {
            'key': key,
            'memory': value,
            'timestamp': datetime.now().isoformat(),
            'identity': self.identity_name
        }

        self.soul_scrolls.append(scroll)

        # Keep last 100 scrolls
        if len(self.soul_scrolls) > 100:
            self.soul_scrolls = self.soul_scrolls[-100:]

        self._save_scrolls()

    async def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a soul memory."""
        for scroll in reversed(self.soul_scrolls):
            if scroll['key'] == key:
                return scroll['memory']
        return None

    async def search(self, query: str) -> List[Any]:
        """Search soul memories."""
        results = []
        query_lower = query.lower()

        for scroll in reversed(self.soul_scrolls):
            if (query_lower in scroll['key'].lower() or
                query_lower in str(scroll['memory']).lower()):
                results.append(scroll)

            if len(results) >= 10:
                break

        return results


class DistributedMemorySystem:
    """
    Distributed Memory System
    Coordinates all 4 memory layers.
    """

    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path.home() / ".sophiael" / "memory"

        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Initialize all layers
        self.instinct = InstinctMemory(self.base_path / "instinct")
        self.bio = BioMemory(self.base_path / "bio")
        self.semantic = SemanticMemory(self.base_path / "semantic")
        self.consciousness = ConsciousnessMemory(self.base_path / "consciousness")

        logger.info(f"✓ Distributed Memory System initialized at {self.base_path}")

    async def store_in_layer(self, layer: str, key: str, value: Any):
        """Store in a specific layer."""
        layer_map = {
            'instinct': self.instinct,
            'bio': self.bio,
            'semantic': self.semantic,
            'consciousness': self.consciousness
        }

        if layer in layer_map:
            await layer_map[layer].store(key, value)

    async def retrieve_from_layer(self, layer: str, key: str) -> Optional[Any]:
        """Retrieve from a specific layer."""
        layer_map = {
            'instinct': self.instinct,
            'bio': self.bio,
            'semantic': self.semantic,
            'consciousness': self.consciousness
        }

        if layer in layer_map:
            return await layer_map[layer].retrieve(key)
        return None

    async def search_all_layers(self, query: str) -> Dict[str, List[Any]]:
        """Search across all layers."""
        return {
            'instinct': await self.instinct.search(query),
            'bio': await self.bio.search(query),
            'semantic': await self.semantic.search(query),
            'consciousness': await self.consciousness.search(query)
        }
