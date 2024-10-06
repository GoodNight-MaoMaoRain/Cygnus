import json
from sqlalchemy.orm import Session
from typing import Optional
from app.orm.models import I18N
from app.schemas.schemas_super_engineer import UpdateLanguageRequest

class CRUDI18N:
    def __init__(self, db: Session):
        self.db = db

    def get_current_language(self) -> Optional[I18N]:
        return self.db.query(I18N).first()

    def update_language(self, i18n: I18N,language_code:str):
        i18n.language_code = language_code
        self.db.commit()
        self.db.refresh(i18n)

    def create_default_language(self) -> I18N:
        i18n = I18N()
        self.db.add(i18n)
        self.db.commit()
        self.db.refresh(i18n)
        return i18n


