from pydantic import BaseModel, ConfigDict
from typing import List, Union, Optional

from sqlalchemy import Column, String, BigInteger, Text

from apps.webui.internal.db import Base, Session

import time
import uuid

####################
# Memory DB Schema
####################


class Memory(Base):
    __tablename__ = "memory"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    content = Column(Text)
    updated_at = Column(BigInteger)
    created_at = Column(BigInteger)


class MemoryModel(BaseModel):
    id: str
    user_id: str
    content: str
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class MemoriesTable:

    def insert_new_memory(
        self,
        user_id: str,
        content: str,
    ) -> Optional[MemoryModel]:
        id = str(uuid.uuid4())

        memory = MemoryModel(
            **{
                "id": id,
                "user_id": user_id,
                "content": content,
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
            }
        )
        result = Memory(**memory.model_dump())
        Session.add(result)
        Session.commit()
        Session.refresh(result)
        if result:
            return MemoryModel.model_validate(result)
        else:
            return None

    def update_memory_by_id(
        self,
        id: str,
        content: str,
    ) -> Optional[MemoryModel]:
        try:
            Session.query(Memory).filter_by(id=id).update(
                {"content": content, "updated_at": int(time.time())}
            )
            Session.commit()
            return self.get_memory_by_id(id)
        except:
            return None

    def get_memories(self) -> List[MemoryModel]:
        try:
            memories = Session.query(Memory).all()
            return [MemoryModel.model_validate(memory) for memory in memories]
        except:
            return None

    def get_memories_by_user_id(self, user_id: str) -> List[MemoryModel]:
        try:
            memories = Session.query(Memory).filter_by(user_id=user_id).all()
            return [MemoryModel.model_validate(memory) for memory in memories]
        except:
            return None

    def get_memory_by_id(self, id: str) -> Optional[MemoryModel]:
        try:
            memory = Session.get(Memory, id)
            return MemoryModel.model_validate(memory)
        except:
            return None

    def delete_memory_by_id(self, id: str) -> bool:
        try:
            Session.query(Memory).filter_by(id=id).delete()
            return True

        except:
            return False

    def delete_memories_by_user_id(self, user_id: str) -> bool:
        try:
            Session.query(Memory).filter_by(user_id=user_id).delete()
            return True
        except:
            return False

    def delete_memory_by_id_and_user_id(self, id: str, user_id: str) -> bool:
        try:
            Session.query(Memory).filter_by(id=id, user_id=user_id).delete()
            return True
        except:
            return False


Memories = MemoriesTable()
