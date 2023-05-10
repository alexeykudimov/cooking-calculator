import logging
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.misc.database import ModelBase

from sqlalchemy.orm import relationship

logger = logging.getLogger(__name__)


class Recipe(ModelBase):
    __tablename__ = 'recipe'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __str__(self):
        return self.name
    

class Component(ModelBase):
    __tablename__ = 'component'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __str__(self):
        return self.name
    

class RecipeComponent(ModelBase):
    __tablename__ = 'recipe_component'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    recipe = relationship("Recipe")
    recipe_id = Column(
            UUID(as_uuid=True), ForeignKey("recipe.id", ondelete='CASCADE'))
    
    component = relationship("Component")
    component_id = Column(
            UUID(as_uuid=True), ForeignKey("component.id", ondelete='CASCADE'))
    
    value = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __str__(self):
        return f"{self.recipe_id}: {self.component_id}"
