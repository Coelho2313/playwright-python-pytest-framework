"""Geração de massa de dados única, garantindo isolamento entre workers xdist."""
import uuid
from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Room:
    """Modelo de quarto para criação via API."""

    room_name: str
    type: str = "Single"
    accessible: bool = True
    description: str = "Quarto criado pela automação"
    image: str = "https://www.mwtestconsultancy.co.uk/img/testim/room2.jpg"
    room_price: int = 150
    features: tuple[str, ...] = ("WiFi", "TV")

    def to_payload(self) -> dict[str, Any]:
        """Converte para o payload esperado pela API."""
        data = asdict(self)
        return {
            "roomName": data["room_name"],
            "type": data["type"],
            "accessible": data["accessible"],
            "description": data["description"],
            "image": data["image"],
            "roomPrice": str(data["room_price"]),
            "features": list(data["features"]),
        }


def unique_room(prefix: str = "QA") -> Room:
    """Cria um quarto com nome único (evita colisão entre workers paralelos)."""
    return Room(room_name=f"{prefix}-{uuid.uuid4().hex[:8]}")
